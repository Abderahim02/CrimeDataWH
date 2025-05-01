-- dim_locations
{{  config(materialized='table',
    alias="dim_locations",
    tags=["dim_locations"]
)
}}

with locations as (
  select distinct
    location as location_id,
    cross_street as location_cross_street,
    LAT as  locations_latitude,
    LON as  locations_longitude
  from {{ source('crime_data_hub', 'crime_data_view') }} --look for source table, geographic data fro LA
  where location is not null
)
select *
from locations
