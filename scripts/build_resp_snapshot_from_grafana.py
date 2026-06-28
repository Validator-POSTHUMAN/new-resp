#!/usr/bin/env python3
"""Build a draft RESP holder snapshot from the public Grafana dashboard API.

The source dashboard stores RESP holder balances in InfluxDB and exposes them
through Grafana's datasource query endpoint. This script keeps the extraction
reproducible without requiring direct InfluxDB access.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import pathlib
import urllib.request
from decimal import Decimal
from typing import Dict, Iterable, List, Optional, Tuple


GRAFANA_QUERY_URL = "https://phmn-stats.posthuman.digital/api/ds/query"
SOURCE_DASHBOARD_URL = (
    "https://phmn-stats.posthuman.digital/d/h50b3TySk/"
    "posthuman-reputation-token-resp-stats"
)
OLD_REPUTATION_SUBDAO_JUNO = (
    "juno1uwmtcc8lxc7waqy9takvnsautlfx5qp688jykvvuk4fezd8jf6fs549ym2"
)
NEW_REPUTATION_SUBDAO_COSMOS = (
    "cosmos1nxxz937qd6zqxllwplydy6hts97c4amaqj8jxa57nsme3dmckk4s3mqujr"
)


CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
CHARSET_MAP = {c: i for i, c in enumerate(CHARSET)}


def bech32_polymod(values: Iterable[int]) -> int:
    generator = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
    chk = 1
    for value in values:
        top = chk >> 25
        chk = (chk & 0x1FFFFFF) << 5 ^ value
        for i in range(5):
            if (top >> i) & 1:
                chk ^= generator[i]
    return chk


def bech32_hrp_expand(hrp: str) -> List[int]:
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


def bech32_verify_checksum(hrp: str, data: List[int]) -> bool:
    return bech32_polymod(bech32_hrp_expand(hrp) + data) == 1


def bech32_create_checksum(hrp: str, data: List[int]) -> List[int]:
    values = bech32_hrp_expand(hrp) + data
    polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 1
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]


def bech32_decode(address: str) -> Tuple[str, List[int]]:
    if address.lower() != address and address.upper() != address:
        raise ValueError(f"mixed-case bech32 address: {address}")
    address = address.lower()
    if not all(33 <= ord(c) <= 126 for c in address):
        raise ValueError(f"invalid bech32 character in address: {address}")
    pos = address.rfind("1")
    if pos < 1 or pos + 7 > len(address):
        raise ValueError(f"invalid bech32 separator/checksum: {address}")
    hrp = address[:pos]
    data = [CHARSET_MAP.get(c, -1) for c in address[pos + 1 :]]
    if any(v == -1 for v in data):
        raise ValueError(f"invalid bech32 data character: {address}")
    if not bech32_verify_checksum(hrp, data):
        raise ValueError(f"bech32 checksum mismatch: {address}")
    return hrp, data[:-6]


def bech32_encode(hrp: str, data: List[int]) -> str:
    combined = data + bech32_create_checksum(hrp, data)
    return hrp + "1" + "".join(CHARSET[d] for d in combined)


def convertbits(data: Iterable[int], frombits: int, tobits: int, pad: bool) -> List[int]:
    acc = 0
    bits = 0
    ret: List[int] = []
    maxv = (1 << tobits) - 1
    max_acc = (1 << (frombits + tobits - 1)) - 1
    for value in data:
        if value < 0 or value >> frombits:
            raise ValueError("invalid bech32 convertbits value")
        acc = ((acc << frombits) | value) & max_acc
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        raise ValueError("invalid bech32 padding")
    return ret


def remap_bech32(address: str, target_hrp: str) -> Tuple[str, int]:
    _hrp, data = bech32_decode(address)
    payload = bytes(convertbits(data, 5, 8, False))
    target_data = convertbits(payload, 8, 5, True)
    return bech32_encode(target_hrp, target_data), len(payload)


def fetch_grafana_resp_owners() -> Dict:
    flux = (
        'from(bucket: "PHMN_addresses")\n'
        '  |> range(start: -2m)\n'
        '  |> filter(fn: (r) => r["_measurement"] == "RESP_owners")\n'
        '  |> filter(fn: (r) => r["_field"] == "RESP")\n'
        "  |> last()"
    )
    payload = {
        "queries": [
            {
                "refId": "A",
                "datasource": {"uid": "ztBlLV37k", "type": "influxdb"},
                "query": flux,
                "rawQuery": True,
                "format": "table",
                "intervalMs": 1000,
                "maxDataPoints": 30000,
            }
        ],
        "from": "now-2m",
        "to": "now",
    }
    data = json.dumps(payload).encode()
    request = urllib.request.Request(
        GRAFANA_QUERY_URL,
        data=data,
        headers={"content-type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode())


def load_grafana_json(path: Optional[pathlib.Path]) -> Dict:
    if path:
        return json.loads(path.read_text())
    return fetch_grafana_resp_owners()


def extract_rows(payload: Dict) -> List[Dict[str, str]]:
    frames = payload["results"]["A"]["frames"]
    rows: List[Dict[str, str]] = []
    for frame in frames:
        fields = frame["schema"]["fields"]
        address = None
        for field in fields:
            if field.get("name") == "RESP":
                address = field.get("labels", {}).get("address")
                break
        if not address:
            continue
        values = frame["data"]["values"]
        timestamp_ms = values[0][0]
        amount = Decimal(str(values[1][0]))
        if amount <= 0:
            continue
        cosmos_address, payload_bytes = remap_bech32(address, "cosmos")
        rows.append(
            {
                "source_timestamp_ms": str(timestamp_ms),
                "source_timestamp_utc": dt.datetime.fromtimestamp(
                    timestamp_ms / 1000, tz=dt.timezone.utc
                ).isoformat(),
                "source_chain": "juno",
                "source_address": address,
                "cosmos_address": cosmos_address,
                "resp_amount": format(amount, "f"),
                "payload_bytes": str(payload_bytes),
                "address_type_hint": (
                    "normal_account_length"
                    if payload_bytes == 20
                    else "contract_or_module_address"
                ),
            }
        )
    rows.sort(key=lambda row: row["source_address"])
    return rows


def load_review_addresses(paths: List[pathlib.Path]) -> Dict[str, Dict[str, str]]:
    review: Dict[str, Dict[str, str]] = {}
    for path in paths:
        if not path.exists():
            continue
        with path.open(newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                lowered = {k: (v or "") for k, v in row.items()}
                address = (
                    lowered.get("address")
                    or lowered.get("old_source_address")
                    or lowered.get("old_address")
                    or ""
                ).strip()
                if not address.startswith("juno1"):
                    continue
                joined = " ".join(lowered.values()).lower()
                if "attacker" in joined or "compromised" in joined or "unauthorized" in joined:
                    review[address] = {
                        "decision": "exclude",
                        "decision_bucket": "incident_attacker_or_compromised",
                        "reason": "Matched PHMN incident attacker/compromised-address evidence.",
                        "evidence_reference": str(path),
                    }
                elif "olim" in joined:
                    review[address] = {
                        "decision": "exclude",
                        "decision_bucket": "olim_operator_requested_exclusion",
                        "reason": "Matched Olim-linked address evidence; operator requested RESP exclusion when a balance exists.",
                        "evidence_reference": str(path),
                    }
                elif "rerouted_to_subdao" in joined:
                    review.setdefault(
                        address,
                        {
                            "decision": "quarantine",
                            "decision_bucket": "previous_subdao_or_treasury_reroute_review",
                            "reason": "Matched prior PHMN SubDAO/treasury reroute row; RESP handling needs operator review.",
                            "evidence_reference": str(path),
                        },
                    )
    return review


def apply_decisions(rows: List[Dict[str, str]], review: Dict[str, Dict[str, str]]) -> None:
    for row in rows:
        source_address = row["source_address"]
        if source_address == OLD_REPUTATION_SUBDAO_JUNO:
            row.update(
                {
                    "decision": "reroute",
                    "decision_bucket": "old_reputation_subdao_treasury",
                    "recipient_cosmos": NEW_REPUTATION_SUBDAO_COSMOS,
                    "reason": "Old RESP Reputation SubDAO treasury; route to the new Reputation SubDAO.",
                    "evidence_reference": SOURCE_DASHBOARD_URL,
                    "notes": "Operator supplied the new Reputation SubDAO address on 2026-06-28.",
                }
            )
            continue
        if source_address in review:
            decision = review[source_address]
            row.update(
                {
                    "decision": decision["decision"],
                    "decision_bucket": decision["decision_bucket"],
                    "recipient_cosmos": "",
                    "reason": decision["reason"],
                    "evidence_reference": decision["evidence_reference"],
                    "notes": "",
                }
            )
            continue
        if row["address_type_hint"] != "normal_account_length":
            row.update(
                {
                    "decision": "quarantine",
                    "decision_bucket": "contract_or_module_review",
                    "recipient_cosmos": "",
                    "reason": "Source address is not a normal 20-byte account; do not distribute to a mechanical Cosmos address without review.",
                    "evidence_reference": SOURCE_DASHBOARD_URL,
                    "notes": "",
                }
            )
            continue
        row.update(
            {
                "decision": "include",
                "decision_bucket": "direct_mechanical_bech32_mapping",
                "recipient_cosmos": row["cosmos_address"],
                "reason": "Normal 20-byte Juno account mapped to Cosmos Hub bech32 with the same payload bytes.",
                "evidence_reference": SOURCE_DASHBOARD_URL,
                "notes": "",
            }
        )


def write_csv(path: pathlib.Path, rows: List[Dict[str, str]], fields: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_summary(path: pathlib.Path, rows: List[Dict[str, str]], generated_at: str) -> Dict:
    by_decision: Dict[str, Dict[str, object]] = {}
    total = Decimal("0")
    for row in rows:
        amount = Decimal(row["resp_amount"])
        total += amount
        bucket = row["decision"]
        entry = by_decision.setdefault(bucket, {"rows": 0, "resp_amount": Decimal("0")})
        entry["rows"] = int(entry["rows"]) + 1
        entry["resp_amount"] = entry["resp_amount"] + amount
    summary = {
        "generated_at_utc": generated_at,
        "source_dashboard": SOURCE_DASHBOARD_URL,
        "old_reputation_subdao_juno": OLD_REPUTATION_SUBDAO_JUNO,
        "new_reputation_subdao_cosmos": NEW_REPUTATION_SUBDAO_COSMOS,
        "holder_rows": len(rows),
        "total_resp": format(total, "f"),
        "by_decision": {
            decision: {
                "rows": value["rows"],
                "resp_amount": format(value["resp_amount"], "f"),
            }
            for decision, value in sorted(by_decision.items())
        },
    }
    path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return summary


def write_report(path: pathlib.Path, summary: Dict) -> None:
    by_decision = summary["by_decision"]
    lines = [
        "# RESP Snapshot Draft - 2026-06-28",
        "",
        "This is a draft RESP holder snapshot built from the public Grafana dashboard datasource.",
        "It is not the final distribution list until operators review quarantine/exclusion rows and publish final checksums.",
        "",
        f"- Source dashboard: {summary['source_dashboard']}",
        f"- Old Reputation SubDAO: {summary['old_reputation_subdao_juno']}",
        f"- New Reputation SubDAO: {summary['new_reputation_subdao_cosmos']}",
        f"- Holder rows: {summary['holder_rows']}",
        f"- Total RESP in holder rows: {summary['total_resp']}",
        "",
        "## Decision Totals",
        "",
    ]
    for decision, value in by_decision.items():
        lines.append(f"- {decision}: {value['rows']} rows, {value['resp_amount']} RESP")
    lines.extend(
        [
            "",
            "## Review Notes",
            "",
            "- include rows are normal 20-byte Juno accounts mapped mechanically to Cosmos Hub bech32.",
            "- exclude rows matched PHMN incident/Olim evidence and should not receive direct new RESP.",
            "- reroute rows are old RESP treasury rows routed to the new Reputation SubDAO.",
            "- quarantine rows require manual review before distribution because they are contract/module-sized addresses or prior treasury/reroute cases.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", type=pathlib.Path)
    parser.add_argument("--repo-root", type=pathlib.Path, default=pathlib.Path("."))
    parser.add_argument("--review-csv", action="append", type=pathlib.Path, default=[])
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    generated_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    payload = load_grafana_json(args.input_json)
    rows = extract_rows(payload)
    review = load_review_addresses(args.review_csv)
    apply_decisions(rows, review)

    fields = [
        "source_timestamp_utc",
        "source_timestamp_ms",
        "source_chain",
        "source_address",
        "cosmos_address",
        "resp_amount",
        "payload_bytes",
        "address_type_hint",
        "decision",
        "decision_bucket",
        "recipient_cosmos",
        "reason",
        "evidence_reference",
        "notes",
    ]
    snapshot = repo / "snapshots" / "resp_snapshot_2026-06-28.csv"
    review_rows = [
        row for row in rows if row["decision"] in {"exclude", "quarantine", "reroute"}
    ]
    distribution_rows = [row for row in rows if row["decision"] in {"include", "reroute"}]
    adjustments = repo / "adjustments" / "resp_excluded_quarantine_reroute_2026-06-28.csv"
    distribution = repo / "snapshots" / "resp_distribution_draft_2026-06-28.csv"
    summary_path = repo / "snapshots" / "resp_snapshot_summary_2026-06-28.json"
    report_path = repo / "reports" / "RESP_SNAPSHOT_DRAFT_2026-06-28.md"

    write_csv(snapshot, rows, fields)
    write_csv(adjustments, review_rows, fields)
    write_csv(distribution, distribution_rows, fields)
    summary = write_summary(summary_path, rows, generated_at)
    write_report(report_path, summary)

    checksum_paths = [snapshot, adjustments, distribution, summary_path, report_path]
    checksums = repo / "checksums" / "SHA256SUMS"
    checksums.write_text(
        "".join(
            f"{sha256(path)}  {path.relative_to(repo)}\n" for path in checksum_paths
        )
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
