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

