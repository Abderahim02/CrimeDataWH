{{ config(
    materialized='table',
    tags=['pub_crime_types']
) }}

select *
from {{ ref('dim_crime_types') }}
