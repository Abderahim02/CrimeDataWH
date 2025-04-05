from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import json
import snowflake.connector
import os
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 4, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

def fetch_and_load():
    url = "https://opensky-network.org/api/states/all"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch data")
    data = response.json()
    timestamp = data.get("time")
    states = data.get("states", [])
    ctx = snowflake.connector.connect(
        user=os.environ.get("SNOWFLAKE_USER"),
        password=os.environ.get("SNOWFLAKE_PASSWORD"),
        account=os.environ.get("SNOWFLAKE_ACCOUNT"),
        warehouse='COMPUTE_WH',
        database='OpenSky',
        schema='PUBLIC'
    )

    cs = ctx.cursor()
    try: # it should be VIEW not TABLE
        cs.execute("""
            CREATE TABLE IF NOT EXISTS open_sky_data (
                id NUMBER AUTOINCREMENT,
                timestamp_uid NUMBER,
                icao24 STRING,
                callsign STRING,
                origin_country STRING,
                time_position NUMBER,
                last_contact NUMBER,
                longitude FLOAT,
                latitude FLOAT,
                baro_altitude FLOAT,
                on_ground BOOLEAN,
                velocity FLOAT,
                true_track FLOAT,
                vertical_rate FLOAT,
                sensors VARIANT,
                geo_altitude FLOAT,
                squawk STRING,
                spi BOOLEAN,
                position_source NUMBER,
                ingestion_time TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP
            )
        """)

        insert_stmt = """
            INSERT INTO open_sky_data (
                timestamp_uid, icao24, callsign, origin_country, time_position, last_contact,
                longitude, latitude, baro_altitude, on_ground, velocity, true_track,
                vertical_rate, sensors, geo_altitude, squawk, spi, position_source
            ) VALUES (
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s
            )
        """

        for state in states:
            cs.execute(insert_stmt, (
                timestamp,
                state[0],  # icao24
                state[1],  # callsign
                state[2],  # origin_country
                state[3],  # time_position
                state[4],  # last_contact
                state[5],  # longitude
                state[6],  # latitude
                state[7],  # baro_altitude
                state[8],  # on_ground
                state[9],  # velocity
                state[10], # true_track
                state[11], # vertical_rate
                state[12], # sensors
                state[13], # geo_altitude
                state[14], # squawk
                state[15], # spi
                state[16]  # position_source
                # state[17]  # aircraft category
                
            ))
    finally:
        cs.close()
        ctx.close()

with DAG(
    'opensky_to_snowflake',
    default_args=default_args,
    schedule_interval='30 8 * * *',
    catchup=False
) as dag:
    
    load_data = PythonOperator(
        task_id='fetch_and_load_data',
        python_callable=fetch_and_load
    )

    load_data
