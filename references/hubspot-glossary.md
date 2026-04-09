# HubSpot Property Glossary

This is the authoritative reference for HubSpot property names used at Pliant. Always resolve property names from this glossary before falling back to the `search_properties` tool.

## Deal properties

| Property | HubSpot field name | Type | Common aliases |
|---|---|---|---|
| Deal name | `dealname` | string | name, deal |
| Deal stage | `name_of_deal_stage` | string | stage, status, pipeline stage. **Use this, NOT `dealstage`** (which returns an internal ID) |
| Pipeline | `pipeline` | string | pipe, sales pipeline |
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

## Deal stage meanings

| Stage | What it means |
|---|---|
| Solution Qualification / Demo conducted | Customer landed in CRM, initial demo done. Early qualification. |
| Pre-Onboarding | Platform registration underway. Account created — waiting on customer. |
| Submitted to credit | Info provided. Pliant Compliance started credit assessment. |
| Info requested | Compliance docs requested. Waiting on customer. |
| Info partially obtained | Some docs received. Waiting on remaining. |
| Info fully obtained | All docs received. Full compliance assessment in progress. |
| Submitted to partner bank | Pre-checked and approved internally. Sent to partner bank for final review. |
| Account activated | Live. Cards can be issued. |
| Closed lost | Dropped out of pipeline. Check loss reason if available. |
| Churned | Was active, decided to leave Pliant. |
