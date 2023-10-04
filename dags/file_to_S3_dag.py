################################
# Modules / Files / Connections
################################
import pandas as pd
from pandas.io.json import json_normalize
import requests
import time
from datetime import datetime, timedelta
from io import StringIO
import os
import boto3

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator

import project_config as cfg
    
################################
# Functions
################################
def pull_bitcoin_data(*args, **kwargs): 
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    response = requests.get(url)
    dictr = response.json()

    time_pulled = dictr['bpi']['USD']
    price = dictr['bpi']['USD']
    df1 = pd.DataFrame(json_normalize(time_pulled))
    df2 = pd.DataFrame(json_normalize(price))
    bitcoin = pd.concat([df1.reset_index(drop=True), df2], axis=1)

    ############### Patch ###############
    #Prep data
    csv_buffer = StringIO()
    bitcoin.to_csv(csv_buffer)
    run_time = time.strftime("%Y-%m-%d_%Hh%Mm%Ss")

    #Create session with boto3.
    session = boto3.Session(aws_access_key_id=cfg.aws["key_id"],
                            aws_secret_access_key=cfg.aws["secret_access_key"],
                            )

    #Creating S3 sesource
    s3 = session.resource('s3')
    object = s3.Object(cfg.aws["bucket_name"], 'bitcoin_{}.csv'.format(run_time))
    result = object.put(Body=csv_buffer.getvalue())

################################
# Airflow Setup
################################
default_args = {
    "owner": "Jake",
    "start_date": datetime(2021, 8, 24),
    "depends_on_past": False,
    "email_on_failure": True,
    "email_on_retry": True,
    "email": "jacob.w.lyman@gmail.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=3)
}

with DAG(dag_id="file_to_S3_dag",
         schedule_interval="*/5 * * * *",
         default_args=default_args,
         template_searchpath=[f"{os.environ['AIRFLOW_HOME']}"],
         catchup=False) as dag:


    ################################
    # Tasks
    ################################
    pull_bitcoin_data = PythonOperator(
        task_id="pull_bitcoin_data",
        python_callable=pull_bitcoin_data
    )

    email = EmailOperator(
        task_id='send_email',
        to='jacob.w.lyman@gmail.com',
        subject='Airflow Confirmation',
        html_content="""<h3>The scheduled file_to_S3_dag.py DAG file was successfully executed!</h3>""",
        dag=dag
    )

    ################################
    # Dependency Chain
    ################################
    pull_bitcoin_data >> email