-- mart_reported_crimes
{{ config(materialized='table') }}

with src as (
  select * from {{ source('crime_data_hub','crime_data_view') }}
),

joined as (

  select
    dr_no                     as reported_crime_id,
    date_rptd as reported_at,
    to_timestamp_ntz(
      to_char(date_occ, 'YYYY-MM-DD') || ' ' || substr(time_occ, 1, 2) || ':' || substr(date_occ, 3, 2),
      'YYYY-MM-DD HH24:MI') as occured_at,
    -- dimension foreign keys
    dpa.police_area_id,
    dct1.crime_type_id        as crime_type_id_1,
    dct2.crime_type_id        as crime_type_id_2,
    dct3.crime_type_id        as crime_type_id_3,
    dct4.crime_type_id        as crime_type_id_4,
    dmo.mo_code_id,
    dcs.case_status_id,
    dlt.location_type_id,
    dw.weapon_id,
    dl.location_id,
    -- degenerate/other attrs
    src.vict_age  as victim_age,
    {{ map_gender('src.vict_sex') }} as victime_sex,
    {{ map_gender('src.VICT_DESCENT') }}  as victime_race

  from src

  left join {{ ref('dim_police_areas') }}   dpa on src.area    = dpa.police_area_id
  left join {{ ref('dim_crime_types') }}    dct1 on src.crm_cd_1    = dct1.crime_type_id
  left join {{ ref('dim_crime_types') }}    dct2 on src.crm_cd_2    = dct2.crime_type_id
  left join {{ ref('dim_crime_types') }}    dct3 on src.crm_cd_3    = dct3.crime_type_id
  left join {{ ref('dim_crime_types') }}    dct4 on src.crm_cd_4    = dct4.crime_type_id
  left join {{ ref('dim_mo_codes') }}       dmo on src.mocodes               = dmo.mo_code_id
  left join {{ ref('dim_case_status') }}    dcs on src.status       = dcs.case_status_id
  left join {{ ref('dim_location_types') }} dlt on src.premis_cd    = dlt.location_type_id
  left join {{ ref('dim_weapons') }}        dw  on src.weapon_used_cd           = dw.weapon_id
  left join {{ ref('dim_locations') }}      dl  on src.location         = dl.location_id

)

select distinct * from joined
