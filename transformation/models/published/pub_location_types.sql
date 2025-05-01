{{ config(
    materialized='table',
    tags=['pub_location_types']
) }}

select *
from {{ ref('dim_location_types') }}
