from datetime import datetime
from airflow import DAG
from airflow.decorators import task, task_group
from airflow.operators.dummy import DummyOperator
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from google.cloud import bigquery
import re

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

project_id = 'double-genius-456516-g6'
dataset_id = 'staging_data'
transform_dataset_id = 'Data_Engineering'
reporting_dataset_id = transform_dataset_id
source_table = f'{project_id}.{dataset_id}.global_data'

def sanitize_name(name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', name.lower())

with DAG(
    dag_id='load_and_transform_view_v2',
    default_args=default_args,
    description='Load a CSV file from GCS to BigQuery and create country-specific tables and views',
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['bigquery', 'gcs', 'csv'],
) as dag:

    check_file_exists = GCSObjectExistenceSensor(
        task_id='check_file_exists',
        bucket='data-engineering-project-11',
        object='uploads/global_health_data_2025-04-27.csv',
        timeout=300,
        poke_interval=30,
        mode='poke',
    )

    load_csv_to_bigquery = GCSToBigQueryOperator(
        task_id='load_csv_to_bq',
        bucket='data-engineering-project-11',
        source_objects=['uploads/global_health_data_2025-04-27.csv'],
        destination_project_dataset_table=source_table,
        source_format='CSV',
        allow_jagged_rows=True,
        ignore_unknown_values=True,
        write_disposition='WRITE_TRUNCATE',
        skip_leading_rows=1,
        field_delimiter=',',
        autodetect=True,
    )

    @task
    def fetch_distinct_countries():
        client = bigquery.Client()
        query = f"SELECT DISTINCT country FROM `{source_table}` WHERE country IS NOT NULL"
        result = client.query(query).result()
        return [row.country for row in result]

    @task
    def generate_table_queries(country):
        safe_country = sanitize_name(country)
        return {
            "table_query": f"""
                CREATE OR REPLACE TABLE `{project_id}.{transform_dataset_id}.{safe_country}_table` AS
                SELECT * FROM `{source_table}`
                WHERE country = '{country}'
            """,
            "view_query": f"""
                CREATE OR REPLACE VIEW `{project_id}.{reporting_dataset_id}.{safe_country}_view` AS
                SELECT 
                    Year AS year, 
                    `Disease Name` AS disease_name, 
                    `Disease Category` AS disease_category, 
                    `Prevalence Rate` AS prevalence_rate, 
                    `Incidence Rate` AS incidence_rate
                FROM `{project_id}.{transform_dataset_id}.{safe_country}_table`
                WHERE `Availability of Vaccines Treatment` = False
            """,
            "country": safe_country
        }

    @task
    def create_table_view(query_dict):
        safe_country = query_dict['country']

        client = bigquery.Client()
        client.query(query_dict['table_query']).result()
        client.query(query_dict['view_query']).result()

        return f"Created table and view for {safe_country}"

    success_task = DummyOperator(task_id='success_task')

    # DAG dependency chain
    countries = fetch_distinct_countries()
    query_dicts = generate_table_queries.expand(country=countries)
    create_table_view.expand(query_dict=query_dicts)

    check_file_exists >> load_csv_to_bigquery >> countries >> query_dicts >> success_task