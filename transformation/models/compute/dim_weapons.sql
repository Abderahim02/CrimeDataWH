-- dim_weapons
{{ config(materialized='table',
    alias="dim_weapons",
    tags=["dim_weapons"]
)
}}

with weapons as (
  select distinct
    weapon_used_cd         as weapon_id,
    weapon_desc as weapon_desc
  from {{ source('crime_data_hub', 'crime_data_view') }}
  where weapon_used_cd is not null
)
select *
from weapons
