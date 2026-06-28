# RESP Migration Snapshot

This repository contains the public RESP migration snapshot from old RESP on
Juno to the new RESP flow on Cosmos Hub.

## Files

- Source holder snapshot:
  [snapshots/resp_snapshot_2026-06-28.csv](snapshots/resp_snapshot_2026-06-28.csv)
- Final 4-column snapshot:
  [snapshots/resp_final_snapshot_2026-06-28.csv](snapshots/resp_final_snapshot_2026-06-28.csv)
- Reputation SubDAO logo:
  [assets/Reputation_subdao_512.png](assets/Reputation_subdao_512.png)
- RESP TokenFactory proposal draft:
  [proposals/RESP_TOKENFACTORY_PROPOSAL.md](proposals/RESP_TOKENFACTORY_PROPOSAL.md)
- Raw Cosmos messages draft:
  [proposals/resp_tokenfactory_messages.json](proposals/resp_tokenfactory_messages.json)
- DAO DAO bulk import JSON:
  [proposals/resp_tokenfactory_daodao_bulk_import.json](proposals/resp_tokenfactory_daodao_bulk_import.json)

## Final Snapshot Format

The final snapshot has only four columns:

- `juno_address`
- `cosmos_address`
- `resp_amount`
- `comment`

Rows without a special comment use a direct Juno-to-Cosmos bech32 mapping with
the same address payload bytes.

## Snapshot Totals

- Holder rows: 1,830
- Total RESP: 1,000,000
- Direct Juno-to-Cosmos mapping: 33,458 RESP
- Routed to the new Reputation SubDAO treasury: 966,542 RESP
- Smart-contract/module source rows routed to the new Reputation SubDAO treasury: 1,805 RESP

## New Reputation SubDAO

- DAO DAO page:
  https://daodao.zone/dao/cosmos1nxxz937qd6zqxllwplydy6hts97c4amaqj8jxa57nsme3dmckk4s3mqujr
- Treasury / recipient address:
  `cosmos1nxxz937qd6zqxllwplydy6hts97c4amaqj8jxa57nsme3dmckk4s3mqujr`
- Planned RESP TokenFactory denom:
  `factory/cosmos1nxxz937qd6zqxllwplydy6hts97c4amaqj8jxa57nsme3dmckk4s3mqujr/RESP`
- Logo URI currently used in the proposal draft:
  https://raw.githubusercontent.com/Validator-POSTHUMAN/new-resp/main/assets/Reputation_subdao_512.png
- Logo SHA-256:
  `f334aeae6c8821c0e3e54edef65b6797f8ccce2e47e4ec2f459bef984a9a4911`

## Old RESP References

- RESP stats dashboard:
  https://phmn-stats.posthuman.digital/d/h50b3TySk/posthuman-reputation-token-resp-stats
- Old Reputation SubDAO treasury:
  https://daodao.zone/dao/juno1uwmtcc8lxc7waqy9takvnsautlfx5qp688jykvvuk4fezd8jf6fs549ym2/treasury
- Old Reputation SubDAO address:
  `juno1uwmtcc8lxc7waqy9takvnsautlfx5qp688jykvvuk4fezd8jf6fs549ym2`

## Routing Rules

- RESP held by normal Juno holder addresses maps to the corresponding Cosmos
  bech32 address.
- RESP held by the old Reputation SubDAO treasury routes to the new Reputation
  SubDAO treasury.
- RESP held by Olim-linked, related, or attacker/incident-linked addresses
  routes to the new Reputation SubDAO treasury.
- RESP held by smart contracts or module-sized Juno source addresses routes to
  the new Reputation SubDAO treasury, not to mechanically converted contract
  addresses.

In this snapshot, these rows are routed to the new Reputation SubDAO treasury:

- old Reputation SubDAO: 964,604 RESP;
- matched Olim-linked address: 133 RESP;
- smart-contract/module source rows: 1,805 RESP.

Total routed to the new Reputation SubDAO treasury: 966,542 RESP.
