# RESP Migration: Cosmos Hub TokenFactory Launch

This repository is the public working area for the planned RESP migration from
the old Juno RESP token to a new Cosmos Hub TokenFactory RESP token.

The repository will publish the migration policy, source snapshots, exclusion
rules, checksums, proposal payloads, and distribution artifacts after they are
verified.

## Current Status

Status: preparation.

The final RESP snapshot has not been published yet. Do not treat any draft
files in this repository as a final distribution list until a final snapshot
CSV and SHA-256 checksum are published.

Known public context:

- RESP stats dashboard:
  https://phmn-stats.posthuman.digital/d/h50b3TySk/posthuman-reputation-token-resp-stats
- Old RESP distribution SubDAO treasury:
  https://daodao.zone/dao/juno1uwmtcc8lxc7waqy9takvnsautlfx5qp688jykvvuk4fezd8jf6fs549ym2/treasury

Planned target:

- Chain: Cosmos Hub
- Token type: TokenFactory
- Symbol: RESP
- New RESP SubDAO: TBD
- New TokenFactory denom: TBD, expected format
  `factory/<new-resp-subdao-cosmos-address>/RESP`

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

The new SubDAO address and final TokenFactory denom are intentionally not filled
in yet. They must be recorded only after the new RESP SubDAO is created and
verified on-chain.

