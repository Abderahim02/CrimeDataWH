-- dim_location_types
{{  config(materialized='table',
    alias="dim_location_types",
    tags=["dim_location_types"]
)
}}

with location_types as (
  select distinct
  premis_cd  as location_type_id,
  premis_cd           as original_premis_code,
  premis_desc as location_type_description
  from {{ source('crime_data_hub', 'crime_data_view') }}
  where premis_cd is not null
)
select *
from location_types
