import hashlib
from airflow.configuration import conf

class MyAirflowUtils:
    @staticmethod    
    def get_correlator(dag_run, task_instance):
        sirius_id = conf.get('core', 'sirius_id')
        dag_run_id = dag_run.id
        task_hash = hashlib.md5(task_instance.task_id.encode()).hexdigest()
        start_date = task_instance.start_date.strftime('%Y%m%d%H%M%S')

        return f"{sirius_id}_{dag_run_id}_{task_hash}_{start_date}"
