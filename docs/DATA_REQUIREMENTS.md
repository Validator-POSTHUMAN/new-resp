# RESP Data Requirements

## Required Source Data

- Old RESP token contract or denom on Juno.
- Old RESP token metadata and total supply.
- Holder list at final snapshot height.
- Old RESP SubDAO treasury balance.
- Any known IBC voucher denoms for RESP, if RESP exists outside Juno.
- Any known pool/LP locations for RESP.
- Confirmed attacker addresses.
- Olim and Olim-linked addresses to check against RESP balances.
- New RESP SubDAO address after creation.
- Intended TokenFactory denom after creation.

## Data Sources To Check

- RESP dashboard:
  https://phmn-stats.posthuman.digital/d/h50b3TySk/posthuman-reputation-token-resp-stats
- Old RESP SubDAO treasury:
  https://daodao.zone/dao/juno1uwmtcc8lxc7waqy9takvnsautlfx5qp688jykvvuk4fezd8jf6fs549ym2/treasury
- Juno RPC / LCD / indexer source used for holder export.
- DAO DAO API or UI for SubDAO treasury verification.
- Any internal POSTHUMAN snapshot/indexer artifacts used for PHMN migration,
  adapted only after RESP-specific validation.

## Open Items

- [ ] Identify old RESP contract or denom.
- [ ] Confirm old RESP total supply.
- [ ] Confirm whether RESP exists on Osmosis, Neutron, or other IBC routes.
- [ ] Confirm whether RESP has liquidity pools or LP holder exposure.
- [ ] Confirm new RESP SubDAO address.
- [ ] Confirm whether new RESP should have a fixed cap and what that cap is.
- [ ] Confirm final treatment of RESP held by the old distribution SubDAO.

