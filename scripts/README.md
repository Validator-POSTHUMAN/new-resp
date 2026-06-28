# RESP Scripts

This directory contains reproducible helper scripts for snapshot and
distribution preparation.

Scripts must not contain secrets.

## build_resp_snapshot_from_grafana.py

Builds the current RESP holder snapshot draft from the public Grafana datasource
query used by the RESP dashboard.

Example:

```bash
./scripts/build_resp_snapshot_from_grafana.py \
  --repo-root . \
  --review-csv /path/to/phmn_incident_seed_addresses_2026-06-18.csv \
  --review-csv /path/to/attacker_olim_interaction_review_2026-06-16.csv \
  --review-csv /path/to/phmn_old_addresses_not_receiving_new_phmn_current.csv
```
