# RESP Snapshot Draft - 2026-06-28

This is a draft RESP holder snapshot built from the public Grafana dashboard datasource.
It is not the final distribution list until operators review quarantine/exclusion rows and publish final checksums.

- Source dashboard: https://phmn-stats.posthuman.digital/d/h50b3TySk/posthuman-reputation-token-resp-stats
- Old Reputation SubDAO: juno1uwmtcc8lxc7waqy9takvnsautlfx5qp688jykvvuk4fezd8jf6fs549ym2
- New Reputation SubDAO: cosmos1nxxz937qd6zqxllwplydy6hts97c4amaqj8jxa57nsme3dmckk4s3mqujr
- Holder rows: 1830
- Total RESP in holder rows: 1000000

## Decision Totals

- exclude: 1 rows, 133 RESP
- include: 1739 rows, 33458 RESP
- quarantine: 89 rows, 1805 RESP
- reroute: 1 rows, 964604 RESP

## Review Notes

- include rows are normal 20-byte Juno accounts mapped mechanically to Cosmos Hub bech32.
- exclude rows matched PHMN incident/Olim evidence and should not receive direct new RESP.
- reroute rows are old RESP treasury rows routed to the new Reputation SubDAO.
- quarantine rows require manual review before distribution because they are contract/module-sized addresses or prior treasury/reroute cases.
