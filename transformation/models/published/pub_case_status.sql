{{ config(
    materialized='table',
    tags=['pub_case_status']
) }}

select *
from {{ ref('dim_case_status') }}
