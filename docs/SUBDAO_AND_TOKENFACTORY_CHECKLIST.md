# RESP SubDAO and TokenFactory Checklist

## Before Creating New RESP

- [ ] New RESP SubDAO exists.
- [ ] New RESP SubDAO treasury address is verified.
- [ ] Governance/multisig policy is known.
- [ ] TokenFactory denom creator/admin path is understood.
- [ ] Cosmos Hub TokenFactory params are checked from live chain state.
- [ ] Denom creation fee and gas requirements are checked.
- [ ] Metadata message format is checked against current Cosmos Hub version.
- [ ] Mint/admin control policy is decided.

## TokenFactory Actions

Draft actions to prepare for DAO DAO proposal review:

- `MsgCreateDenom`
- `MsgSetDenomMetadata`
- `MsgMint`
- optional `MsgChangeAdmin`
- distribution transfer actions or batched spend actions

The exact payloads must be generated only after the new RESP SubDAO address and
final denom are known.

## Distribution Checks

- [ ] Final CSV is reviewed.
- [ ] Final CSV checksum is published.
- [ ] Sum of distribution rows matches approved policy.
- [ ] Excluded rows receive no direct distribution.
- [ ] Quarantine rows are routed to the approved handling bucket or left
      unresolved.
- [ ] Batch sizes are safe for DAO DAO proposal execution and gas.
- [ ] A small dry-run or generate-only rehearsal is completed.

