# Proposal: Create RESP TokenFactory Denom

## Target DAO

New Reputation SubDAO:

https://daodao.zone/dao/cosmos1nxxz937qd6zqxllwplydy6hts97c4amaqj8jxa57nsme3dmckk4s3mqujr

## Proposal Title

Create new RESP TokenFactory token on Cosmos Hub

## Proposal Summary

This proposal creates the new RESP token on Cosmos Hub using TokenFactory,
sets the bank metadata for RESP, and mints the migration supply to the new
Reputation SubDAO treasury.

The new token replaces the old RESP accounting on Juno for the migration flow.
The final migration snapshot is published in this repository:

https://github.com/Validator-POSTHUMAN/new-resp

## Token Parameters

- Chain: Cosmos Hub
- Chain ID: cosmoshub-4
- Token type: TokenFactory SDK coin
- Creator/admin: cosmos1nxxz937qd6zqxllwplydy6hts97c4amaqj8jxa57nsme3dmckk4s3mqujr
- Subdenom: RESP
- Base denom: factory/cosmos1nxxz937qd6zqxllwplydy6hts97c4amaqj8jxa57nsme3dmckk4s3mqujr/RESP
- Display denom: resp
- Symbol: RESP
- Exponent: 6
- Name: POSTHUMAN Reputation
- Description: POSTHUMAN Reputation token (RESP) on Cosmos Hub.

## Logo

Current logo URL:

https://raw.githubusercontent.com/Validator-POSTHUMAN/new-resp/main/assets/Reputation_subdao_512.png

Logo SHA-256:

f334aeae6c8821c0e3e54edef65b6797f8ccce2e47e4ec2f459bef984a9a4911

IPFS note: the proposal currently uses the GitHub raw logo URL because no
verified IPFS CID has been pinned from this workspace. If the logo is pinned to
IPFS before proposal submission, replace the metadata uri with the verified
ipfs://... URI and keep the same uri_hash only if the pinned bytes match
assets/Reputation_subdao_512.png.

## Mint Amount

The final RESP snapshot total is 1,000,000 RESP.

With exponent 6, the TokenFactory base-unit mint amount is:

1000000000000

Mint recipient:

cosmos1nxxz937qd6zqxllwplydy6hts97c4amaqj8jxa57nsme3dmckk4s3mqujr

## Snapshot References

- Source holder snapshot:
  snapshots/resp_snapshot_2026-06-28.csv
- Final four-column snapshot:
  snapshots/resp_final_snapshot_2026-06-28.csv
- Final snapshot SHA-256:
  19e48ea856994332d69caafdc605768ee5b093a78e19ad7cc38d7dc0e0fe0ea7

Final snapshot routing summary:

- total: 1,000,000 RESP;
- normal holder direct mapping: 33,458 RESP;
- routed to the new Reputation SubDAO treasury: 966,542 RESP;
- old Reputation SubDAO treasury routed amount: 964,604 RESP;
- matched Olim-linked routed amount: 133 RESP;
- smart-contract/module source rows routed amount: 1,805 RESP.

## Proposed Actions

1. Create TokenFactory denom RESP.
2. Set bank metadata for factory/cosmos1nxxz937qd6zqxllwplydy6hts97c4amaqj8jxa57nsme3dmckk4s3mqujr/RESP.
3. Mint 1000000000000 base units to the new Reputation SubDAO treasury.

Distribution to snapshot recipients should be handled by a separate reviewed
proposal or batch after the denom exists and the mint transaction is verified.

## Raw Message Draft

DAO DAO bulk import JSON:

proposals/resp_tokenfactory_daodao_bulk_import.json

This is the file to paste into DAO DAO Bulk Import Actions.

Raw Cosmos message draft for review:

proposals/resp_tokenfactory_messages.json
