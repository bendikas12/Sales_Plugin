## 0.2.1 - 2026-04-09
- Fixed: hubspot-record-analysis — corrected field names to `expected_monthly_transaction_volume` and `total_addressable_monthly_transaction_volume`
- Fixed: hubspot-record-analysis — use `name_of_deal_stage` instead of `dealstage` to get human-readable stage label
- Fixed: hubspot-record-analysis — Activity objectType unsupported; now queries Email, Note, Call separately and merges results
- Fixed: hubspot-record-analysis — skill now fetches record without properties first to discover schema before presenting results

## 0.2.0 - 2026-04-08
- Added: hubspot-record-analysis skill — analyze deals, contacts, or companies by name, ID, or HubSpot URL

## 0.1.1 - 2026-04-08
- Changed: renamed plugin from "nexus" to "sales-plugin"

## 0.1.0 - 2026-04-08
- Initial release: sales-dashboard, deal-prep, email-followup skills
