{{ config(
    materialized='table',
    tags=['pub_locations']
) }}

select *
from {{ ref('dim_locations') }}
