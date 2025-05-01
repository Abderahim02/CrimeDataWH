-- dim_police_areas
{{  config(materialized='table',
    alias="dim_police_areas",
    tags=["dim_police_areas"]
)
}}

with police_areas as ( 
  select distinct
    area as police_area_id,
    area_name as police_area_name,
    substring(rpt_dist_no, 1, 1) as main_police_areas_code
    -- look for source table, for police areas
  from {{ source('crime_data_hub', 'crime_data_view') }}
  where area is not null
)
select *
from police_areas