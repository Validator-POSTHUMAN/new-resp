# RESP Migration Plan

## Objective

Prepare a public and auditable migration from old RESP on Juno to new RESP on
Cosmos Hub as a TokenFactory denom.

The intended process mirrors the PHMN migration pattern, adapted to RESP:

1. Freeze the source accounting point with a public snapshot.
2. Identify all old RESP ownership rows.
3. Exclude attacker-controlled rows.
4. Exclude or quarantine Olim-linked rows that hold RESP, based on evidence.
5. Resolve SubDAO, contract, IBC, module, and other non-standard holders.
6. Publish final CSV and checksums.
7. Create the new RESP TokenFactory denom from the new RESP SubDAO.
8. Set token metadata.
9. Mint the reviewed amount under DAO/SubDAO control.
10. Distribute new RESP according to the final published snapshot.

## Known Inputs

- Old RESP stats dashboard:
  https://phmn-stats.posthuman.digital/d/h50b3TySk/posthuman-reputation-token-resp-stats
- Old RESP distribution SubDAO treasury:
  https://daodao.zone/dao/juno1uwmtcc8lxc7waqy9takvnsautlfx5qp688jykvvuk4fezd8jf6fs549ym2/treasury

## Required Decisions

- New RESP SubDAO address.
- New RESP TokenFactory admin policy.
- Final snapshot height and timestamp.
- Whether any old RESP transfers after final snapshot publication are ignored.
- Whether to mint exactly the eligible distribution amount or a larger capped
  supply with reserves held by the new RESP SubDAO.
- Final treatment of attacker, Olim-linked, weak-link, and quarantine rows.

## Required Artifacts

- Source snapshot CSV.
- Address mapping CSV from Juno/IBC holder rows to Cosmos Hub destinations.
- Exclusion list with evidence references.
- Quarantine/manual-review list with reasons.
- Final distribution CSV.
- SHA-256 checksum manifest.
- DAO DAO proposal payloads for TokenFactory launch and distribution.
- Public report explaining the final rules.

## Initial Work Queue

- [ ] Verify old RESP token contract/denom and total supply.
- [ ] Export current RESP holder set from Juno and any known IBC locations.
- [ ] Identify old SubDAO treasury RESP balances.
- [ ] Collect confirmed attacker addresses from PHMN incident evidence and RESP
      specific evidence.
- [ ] Collect Olim and Olim-linked addresses to check against RESP balances.
- [ ] Build candidate snapshot.
- [ ] Build exclusion/quarantine draft.
- [ ] Build final distribution draft.
- [ ] Review with operators before publishing final snapshot.

