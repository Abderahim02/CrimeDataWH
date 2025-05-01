from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import snowflake.connector
import os

LOAD_DATA_SCRIPT_PATH = '/home/lagraoui/CrimeData/dags/scripts/load_data.pw1'
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 4, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

def create_view():
    ctx = snowflake.connector.connect(
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        warehouse='COMPUTE_WH',
        database='CrimeData',
        schema='PUBLIC'
    )
    cs = ctx.cursor()
    try:
        cs.execute("""
         CREATE OR REPLACE VIEW crime_data_view AS
            SELECT
                t.$1::VARCHAR                AS dr_no,
                TO_TIMESTAMP(t.$2, 'MM/DD/YYYY HH12:MI:SS AM') AS date_rptd,
                TO_TIMESTAMP(t.$3, 'MM/DD/YYYY HH12:MI:SS AM') AS date_occ,
                t.$4          AS time_occ,
                t.$5         AS area,
                t.$6                         AS area_name,
                t.$7                         AS rpt_dist_no,
                t.$8        AS part_1_2,
                t.$9                         AS crm_cd,
                t.$10                        AS crm_cd_desc,
                t.$11                        AS mocodes,
                t.$12        AS vict_age,
                t.$13                        AS vict_sex,
                t.$14                        AS vict_descent,
                t.$15       AS premis_cd,
                t.$16                        AS premis_desc,
                t.$17                        AS weapon_used_cd,
                t.$18                        AS weapon_desc,
                t.$19                        AS status,
                t.$20                        AS status_desc,
                t.$21                        AS crm_cd_1,
                t.$22                        AS crm_cd_2,
                t.$23                        AS crm_cd_3,
                t.$24                        AS crm_cd_4,
                t.$25                        AS location,
                t.$26                        AS cross_street,
                t.$27          AS lat,
                t.$28         AS lon
            FROM @CRIMEDATA.PUBLIC.CRIME_DATA_SOURCE (FILE_FORMAT => 'my_csv_format') t;
        """)
    finally:
        cs.close()
        ctx.close()

with DAG(
    'crime_data_to_snowflake',
    default_args=default_args,
    schedule_interval='30 8 */15 * *',
    catchup=False,
) as dag:

    # download full CSV via PowerShell pagination script
    download_crime_data = BashOperator(
        task_id='download_crime_data',
        bash_command=f"""
            pwsh -File {LOAD_DATA_SCRIPT_PATH}
        """
    )

    # PUT in stage #define SNOWSQL_PWD in the environment
    stage = BashOperator(
        task_id='stage_and_copy',
        bash_command=r"""
    snowsql \
    --config ~/.snowsql/config \
    -q "
        CREATE OR REPLACE FILE FORMAT my_csv_format 
            TYPE = 'CSV' 
            FIELD_DELIMITER = ',' 
            SKIP_HEADER = 1 
            FIELD_OPTIONALLY_ENCLOSED_BY = '\"'
            TRIM_SPACE = TRUE
            ESCAPE_UNENCLOSED_FIELD = NONE;
        drop view CRIMEDATA.PUBLIC.CRIME_DATA_VIEW;
        PUT file:///tmp/lapd_crime_data_all.csv @CRIMEDATA.PUBLIC.CRIME_DATA_SOURCE AUTO_COMPRESS=TRUE;"
        """
    )

    # create the view 
    build_view = PythonOperator(
        task_id='create_view',
        python_callable=create_view,
    )

    download_crime_data >> stage >> build_view
