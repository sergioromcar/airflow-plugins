from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'use_plugin_macro_example',
    default_args=default_args,
    description='Ejemplo de DAG utilizando un plugin macro',
    schedule_interval='@daily',
)

use_plugin_macro = BashOperator(
    task_id="use_plugin_macro",
    #bash_command="echo {{ macros.macros01_plugin.get_data() }}",
    bash_command="echo '{{ macros.macros01_plugin.get_correlator(dag_run,task_instance) }}' ",
    dag=dag,
)

