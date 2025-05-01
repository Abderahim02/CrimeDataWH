{{ config(
    materialized='table',
    tags=['pub_mo_codes']
) }}

select *
from {{ ref('dim_mo_codes') }}
