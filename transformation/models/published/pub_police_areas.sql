{{ config(
    materialized='table',
    tags=['pub_police_areas']
) }}

select *
from {{ ref('dim_police_areas') }}
