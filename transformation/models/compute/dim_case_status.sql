-- dim_case_status
{{  config(materialized='table',
    alias="dim_case_status",
    tags=["dim_case_status"]
)
}}

with case_status as (
  select distinct
    status     as case_status_id,
    NULL as case_status_description -- lok for source table
  from {{ source('crime_data_hub', 'crime_data_view') }}
  where status is not null
)
select *
from case_status
