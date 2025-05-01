-- dim_crime_types
{{ config(
    materialized='table',
    alias="dim_crime_types",
    tags=["dim_crime_types"]
) }}

select distinct
  crm_cd     as crime_type_id,
  crm_cd as crime_code,
  crm_cd_desc as crime_description,
  part_1_2
from {{ source('crime_data_hub', 'crime_data_view') }}
where crm_cd is not null
