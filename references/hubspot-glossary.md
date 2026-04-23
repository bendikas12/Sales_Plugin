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

### Sales Pipeline (`16177355`)

| Stage label | `dealstage` ID |
|---|---|
| Discovery / Demo Scheduled | `16177356` |
| Solution Qualification / Demo conducted | `16177357` |
| Business Case Validation | `4148324547` |
| Commercial Alignment | `4148324548` |
| Pre-Onboarding | `4148324549` |
| Submitted to credit | `1515896` |
| Info requested | `1515897` |
| Info partially obtained | `35178338` |
| Info fully obtained | `1515898` |
| Submitted to partner bank | `1515899` |
| Account activated | `16177379` |
| Closed Lost | `16258181` |
| Churned | `30637484` |

Rows marked `TODO_FILL_IN` need to be populated from HubSpot (Settings → Objects → Deals → Pipelines → Sales Pipeline, then inspect the stage URL or API). Until populated, skills that need these IDs should either ask the user or fall back to filtering on `name_of_deal_stage` labels.

## Stage-entered timestamp properties

HubSpot (Pliant custom) exposes per-stage "date entered" timestamp properties on deals with internal names of the form `deal_stage_timestamp_<something>`. Use these to filter deals by when they *entered* a stage, regardless of where they are now.

| Stage label | Internal name |
|---|---|
| Discovery / Demo Scheduled | `TODO_DISCOVER_AT_RUNTIME` |
| Submitted to credit | `TODO_DISCOVER_AT_RUNTIME` |
| Account activated | `TODO_DISCOVER_AT_RUNTIME` |

Rows marked `TODO_DISCOVER_AT_RUNTIME` must be resolved via `search_properties` on the `Deal` object, filtered by internal name prefix `deal_stage_timestamp` and matched against the stage label above. Skills that need these should discover them at runtime and can optionally cache the resolved names back into this table in a follow-up change.

## Deal stage meanings

| Stage | What it means |
|---|---|
| Discovery / Demo Scheduled | Demo call is scheduled. |
| Solution Qualification / Demo conducted | Customer landed in CRM, initial demo done. Early qualification. |
| Business Case Validation |
| Commercial Alignment |
| Pre-Onboarding | Platform registration underway. Account created — waiting on customer. |
| Submitted to credit | Info provided. Pliant Compliance started credit assessment. |
| Info requested | Compliance docs requested. Waiting on customer. |
| Info partially obtained | Some docs received. Waiting on remaining. |
| Info fully obtained | All docs received. Full compliance assessment in progress. |
| Submitted to partner bank | Pre-checked and approved internally. Sent to partner bank for final review. |
| Account activated | Live. Cards can be issued. |
| Closed lost | Dropped out of pipeline. Check loss reason if available. |
| Churned | Was active, decided to leave Pliant. |
