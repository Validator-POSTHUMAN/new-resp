# RESP Snapshot Policy

## Purpose

The final RESP snapshot is the source of truth for new RESP distribution.

Until the final snapshot and checksum are published, all balances and
distribution files are draft-only.

## Snapshot Rule

The final snapshot must record:

- source chain;
- source address;
- source token contract or denom;
- amount;
- source height;
- source timestamp;
- mapped Cosmos Hub destination address, when safe;
- row type;
- handling decision;
- notes/evidence reference.

## Post-Snapshot Transfers

After the final snapshot is published, old RESP transfers should not change the
new RESP distribution unless operators explicitly publish a corrected snapshot.

This prevents last-minute manipulation and makes the migration auditable.

## Address Mapping

Plain account addresses may be bech32-mapped only when the underlying account
ownership is clear.

Do not mechanically map these row types without review:

- DAO and SubDAO treasury addresses;
- CosmWasm contracts;
- module accounts;
- IBC escrow accounts;
- pool and LP-related accounts;
- multisigs with unclear destination policy;
- centralized exchange or custodial accounts;
- attacker-linked or Olim-linked accounts.

## Required Final Files

Expected final publication files:

- `snapshots/resp_final_snapshot.csv`
- `snapshots/resp_final_distribution.csv`
- `snapshots/resp_final_distribution_summary.json`
- `adjustments/resp_excluded_addresses.csv`
- `adjustments/resp_quarantine_rows.csv`
- `checksums/SHA256SUMS`

## Minimum Review Checks

- Sum source rows and final distribution rows.
- Confirm excluded rows do not receive direct new RESP.
- Confirm quarantine rows are routed to a DAO/SubDAO handling bucket or left
  pending.
- Confirm SubDAO treasury rows route to the new intended SubDAO destinations.
- Confirm no unsupported contract/module/pool row is sent to a dead converted
  Cosmos Hub address.
- Confirm checksums match the published files.

