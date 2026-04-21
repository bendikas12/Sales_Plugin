# HubSpot Property Glossary

This is the authoritative reference for HubSpot property names used at Pliant. Always resolve property names from this glossary before falling back to the `search_properties` tool.

## Deal properties

| Property | HubSpot field name | Type | Common aliases |
|---|---|---|---|
| Deal name | `dealname` | string | name, deal |
| Deal stage | `name_of_deal_stage` | string | stage, status, pipeline stage. **Use this, NOT `dealstage`** (which returns an internal ID) |
| Pipeline | `pipeline` | enumeration | pipe, sales pipeline. **Returns an ID — use the lookup table below to get the human-readable name** |
| Expected monthly transaction volume | `expected_monthly_transaction_volume` | number | expected trx, expected volume, monthly trx, expected monthly trx |
| Total addressable monthly transaction volume | `total_addressable_monthly_transaction_volume` | number | addressable volume, addressable trx, total addressable, TAM volume |
| Trx volume (last 0–30 days) | `trx_vol_last_0_to_30_days` | number | last 30 days trx, recent volume, this month trx |
| Trx volume (last 31–60 days) | `trx_vol_last_31_to_60_days` | number | last 31-60 trx, previous month trx |
| Trx volume (last 61–90 days) | `trx_vol_last_61_to_90_days` | number | last 61-90 trx, two months ago trx |
| Trx volume (last 0–180 days) | `trx_vol_last_0_to_180_days` | number | last 180 days trx, half year trx, 6 month trx |
| Close date | `closedate` | date | close, closing date, activation date |
| Owner | `hubspot_owner_id` | string | sales rep, rep, assigned to, deal owner |
| Vertical | `vertical` | string | industry, sector |
| Sub-Vertical | `sub_vertical` | string | sub-industry, segment |
| Country | `country` | string | region, location, market |

## Contact properties

| Property | HubSpot field name | Type | Common aliases |
|---|---|---|---|
| First name | `firstname` | string | first, given name |
| Last name | `lastname` | string | last, surname, family name |
| Email | `email` | string | email address, mail |
| Job title | `jobtitle` | string | title, role, position |
| Phone | `phone` | string | phone number, tel, mobile |
| Owner | `hubspot_owner_id` | string | rep, assigned to, contact owner |
| Country/Region | `country_region` | string | country, region, location |

## Company properties

| Property | HubSpot field name | Type | Common aliases |
|---|---|---|---|
| Name | `name` | string | company name, org |
| Domain | `domain` | string | website, URL |
| Vertical | `vertical` | string | industry, sector |
| Sub-Vertical | `sub_vertical` | string | sub-industry, segment |
| Country/Region | `country_region` | string | country, region, location |
| Owner | `hubspot_owner_id` | string | rep, assigned to, account owner |

## Pipeline ID lookup

The `pipeline` field returns a numeric ID. Use this table to resolve it to a name:

| Pipeline ID | Pipeline Name |
|---|---|
| `14755466` | Pre-Sales Pipeline |
| `16177355` | Sales Pipeline |
| `4015640` | Referrer |
| `18930566` | Partner Team |
| `25225019` | Banking |
| `1928248520` | Insurance |

## Deal stage ID lookup

The `dealstage` field returns an internal ID. Prefer filtering on these IDs rather than `name_of_deal_stage` labels — IDs are stable across label renames and localisations.

| Stage label | `dealstage` ID |
|---|---|
| Account activated | `16177379` |
| Closed Lost | `16258181` |
| Churned | `30637484` |

Additional stage IDs can be added here as other skills need them.

## Deal stage meanings

| Stage | What it means |
|---|---|
| Discovery / Demo Scheduled | First contact made and discovery / demo is on the calendar but hasn't happened yet. |
| Solution Qualification / Demo conducted | Customer has landed in the CRM and initial demo has been conducted. Early qualification phase. |
| Business Case Validation | Post-demo. Validating the business case — ROI, use-cases, fit — before commercial discussion. |
| Commercial Alignment | Business case accepted. Aligning on pricing, terms, and commercial structure. |
| Pre-Onboarding | Client is in pre-onboarding. Platform registration (transaction link) is underway. Account has been created — waiting on customer to proceed. |
| Submitted to credit | All initial information has been provided and filled out. Pliant Compliance has started the credit assessment. |
| Info requested | Compliance documents have been requested. Waiting on the customer to submit. |
| Info partially obtained | Some compliance documents have been received. Waiting on customer to provide the remaining documents. |
| Info fully obtained | All compliance documents have been received. Pliant Compliance is continuing the full assessment. |
| Submitted to partner bank | Customer has been pre-checked and approved internally. Deal has been submitted to the partner bank for final review. |
| Account activated | Account is ready to use. Cards can be issued. Deal is live. |
| Closed lost | Deal has dropped out of the pipeline. Check the loss reason property if available. |
| Churned | Customer was active but decided to leave Pliant. |
