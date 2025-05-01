-- dim_mo_codes
{{ config(materialized='table',
    alias="dim_mo_codes",
    tags=["dim_mo_codes"]
)
}}


with mo_codes as (
  select distinct
    mocodes        as mo_code_id,
    NULL as mo_description -- look for source table
  from {{ source('crime_data_hub', 'crime_data_view') }}
  where mocodes is not null
)
select *
from mo_codes
