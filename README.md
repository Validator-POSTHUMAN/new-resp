# RESP Migration: Cosmos Hub TokenFactory Launch

This repository is the public working area for the planned RESP migration from
the old Juno RESP token to a new Cosmos Hub TokenFactory RESP token.

The repository will publish the migration policy, source snapshots, exclusion
rules, checksums, proposal payloads, and distribution artifacts after they are
verified.

## Current Status

Status: draft snapshot published, final review pending.

The current RESP holder snapshot draft is published in
`snapshots/resp_snapshot_2026-06-28.csv`. Do not treat it as the final
distribution list until quarantine/exclusion rows are reviewed and a final
snapshot CSV is explicitly published.

Known public context:

- RESP stats dashboard:
  https://phmn-stats.posthuman.digital/d/h50b3TySk/posthuman-reputation-token-resp-stats
- Old RESP distribution SubDAO treasury:
  https://daodao.zone/dao/juno1uwmtcc8lxc7waqy9takvnsautlfx5qp688jykvvuk4fezd8jf6fs549ym2/treasury

Planned target:

- Chain: Cosmos Hub
- Token type: TokenFactory
- Symbol: RESP
- New RESP SubDAO:
  https://daodao.zone/dao/cosmos1nxxz937qd6zqxllwplydy6hts97c4amaqj8jxa57nsme3dmckk4s3mqujr
- New TokenFactory denom: TBD, expected format
  `factory/cosmos1nxxz937qd6zqxllwplydy6hts97c4amaqj8jxa57nsme3dmckk4s3mqujr/RESP`

## Current Draft Snapshot

- Snapshot CSV: `snapshots/resp_snapshot_2026-06-28.csv`
- Draft distribution CSV: `snapshots/resp_distribution_draft_2026-06-28.csv`
- Exclusion/quarantine/reroute rows:
  `adjustments/resp_excluded_quarantine_reroute_2026-06-28.csv`
- Summary JSON: `snapshots/resp_snapshot_summary_2026-06-28.json`
- Review report: `reports/RESP_SNAPSHOT_DRAFT_2026-06-28.md`
- Checksums: `checksums/SHA256SUMS`

Draft totals:

- Holder rows: 1,830
- Total RESP: 1,000,000
- Direct include: 1,739 rows / 33,458 RESP
- Old Reputation SubDAO reroute: 1 row / 964,604 RESP
- Olim/incident exclusion: 1 row / 133 RESP
- Quarantine/manual review: 89 rows / 1,805 RESP

## Migration Principles

- Use a public, reproducible snapshot.
- Preserve verified legitimate ownership.
- Exclude confirmed attacker-controlled RESP balances.
- Exclude or quarantine RESP balances held by Olim-linked addresses when the
  evidence and snapshot show they hold RESP.
- Treat weak links, contracts, module accounts, pool accounts, IBC escrows,
  and ambiguous rows as manual-review or quarantine rows instead of sending to
  mechanically converted addresses.
- Publish checksums for final artifacts before distribution.
- Keep old RESP post-snapshot transfers irrelevant to the new-token
  distribution after the final snapshot is published.
- Execute TokenFactory creation, metadata, minting, and distribution through
  reviewable DAO DAO / SubDAO proposal artifacts where possible.

## Repository Layout

- `docs/` - migration policy and operational planning.
- `snapshots/` - final and intermediate snapshot CSV/JSON artifacts.
- `adjustments/` - exclusion, quarantine, reroute, and reconciliation files.
- `reports/` - public reports and review notes.
- `inputs/` - operator-provided seed lists and source references.
- `proposals/` - DAO DAO proposal payloads and review checklists.
- `scripts/` - reproducible helper scripts.
- `checksums/` - SHA-256 manifests for published artifacts.

## First Documents

- [Migration plan](docs/MIGRATION_PLAN.md)
- [Snapshot policy](docs/SNAPSHOT_POLICY.md)
- [Exclusions and quarantine policy](docs/EXCLUSIONS_AND_QUARANTINE.md)
- [Data requirements](docs/DATA_REQUIREMENTS.md)
- [SubDAO and TokenFactory checklist](docs/SUBDAO_AND_TOKENFACTORY_CHECKLIST.md)

## Operator Notes

The new RESP SubDAO address is recorded. The TokenFactory denom remains pending
until the denom is created or confirmed on-chain.
