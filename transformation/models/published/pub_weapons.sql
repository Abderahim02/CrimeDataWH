{{ config(
    materialized='table',
    tags=['pub_weapons']
) }}

select *
from {{ ref('dim_weapons') }}
