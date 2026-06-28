# RESP Exclusions and Quarantine Policy

## Scope

This document defines the initial policy for addresses that should not receive
new RESP directly during migration.

The final address lists must be published as CSV files with evidence links or
internal evidence references.

## Excluded Rows

Exclude rows only when the evidence is strong enough.

Initial exclusion categories:

- confirmed attacker-controlled RESP balances;
- compromised or unauthorized-mint related addresses, if applicable to RESP;
- Olim-linked addresses when they hold RESP and operator-approved evidence
  supports exclusion;
- addresses explicitly approved for exclusion by POSTHUMAN operators.

## Quarantine Rows

Quarantine rows when ownership or recipient mapping is unclear.

Initial quarantine categories:

- weak attacker links;
- weak Olim links;
- contract addresses;
- DAO/SubDAO addresses pending reroute decision;
- module accounts;
- IBC escrow accounts;
- LP/pool/proxy accounts;
- addresses that cannot be safely mapped to Cosmos Hub.

Quarantine means: do not distribute directly to the old holder row until the
row is resolved.

## Evidence Standard

Each exclusion or quarantine row should include:

- old address;
- chain;
- amount;
- reason;
- evidence type;
- evidence reference;
- confidence: high, medium, or low;
- operator decision status.

High-confidence rows may be excluded directly.

Medium/low-confidence rows should normally be quarantined for manual review.

## Draft CSV Schema

```csv
chain,address,amount,category,decision,confidence,evidence_reference,notes
```

Decision values:

- `exclude`
- `quarantine`
- `reroute`
- `include`

## Current Draft Rows

The current draft review file is:

- `adjustments/resp_excluded_quarantine_reroute_2026-06-28.csv`

Current draft treatment:

- old Reputation SubDAO treasury
  `juno1uwmtcc8lxc7waqy9takvnsautlfx5qp688jykvvuk4fezd8jf6fs549ym2`
  reroutes 964,604 RESP to the new Reputation SubDAO
  `cosmos1nxxz937qd6zqxllwplydy6hts97c4amaqj8jxa57nsme3dmckk4s3mqujr`;
- Olim-linked `juno1eltl6qu6y538vhux3mk3pjpn7redx8najm4u3e` holds
  133 RESP and is marked excluded per operator request;
- 89 contract/module-sized holder rows totaling 1,805 RESP are quarantined for
  manual review instead of receiving direct mechanically converted Cosmos
  addresses.
