import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta


default_args = {
    'owner': 'Enzo',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'schedule_interval': None,
    'retry_delay': timedelta(minutes=5),
}
dag = DAG(
   'magicbox',
   default_args=default_args,
   description='MagicBox DAG',
   schedule_interval= None,
# schedule_interval=timedelta(days=1)
)


t4a_command = "/home/enzo/scripts/builder.sh "

t4a= BashOperator(
    task_id='Docker_DB_Build',
    depends_on_past=False,
    bash_command=t4a_command,
    dag=dag)


t4c_command = "/home/enzo/scripts/benchmark.sh "

t4c= BashOperator(
    task_id='Benchmark_Logs',
    depends_on_past=False,
    bash_command=t4c_command,
    dag=dag)


t3a = BashOperator(
    task_id='Coping_DB',
    depends_on_past=False,
    bash_command='cp /home/enzo/tech_view/database.sql /home/enzo/Builder ',
    dag=dag)

t2_command = "/home/enzo/scripts/unzipscript.sh "

t2 = BashOperator(
    task_id='Unzip_Techout',
    depends_on_past=False,
    bash_command=t2_command,
    dag=dag)



t5a = BashOperator(
    task_id='Docker_Compose_DB',
    depends_on_past=False,
    bash_command='docker-compose -f /home/enzo/composers/dbs/docker-compose.yml up -d ',
    dag=dag)

t3b = BashOperator(
    task_id='Docker_Compose_Elasticsearch',
    depends_on_past=False,
    bash_command='docker-compose -f /home/enzo/composers/elasticsearch/docker-compose.yml up -d ',
    dag=dag)


t1_command = "/home/enzo/scripts/clearner.sh "

t1 = BashOperator(
    task_id='Cleaning',
    depends_on_past=False,
    bash_command=t1_command,
    dag=dag)

t4b_command = "/home/enzo/scripts/start_logstash.sh "

t4b = BashOperator(
    task_id='Starts_Logstasth',
    depends_on_past=False,
    bash_command=t4b_command,
    dag=dag)

t6b_command = "/home/enzo/scripts/mapper.sh "

t6b = BashOperator(
    task_id='Mapping_index_Elasticsearch',
    depends_on_past=False,
    bash_command=t6b_command,
    dag=dag)

t5b_command = "/home/enzo/scripts/start_filebeat.sh "

t5b = BashOperator(
    task_id='Starting_Filebeat',
    depends_on_past=False,
    bash_command=t5b_command,
    dag=dag)


t6a_command = "/home/enzo/scripts/log_starter.sh "

t6a = BashOperator(
    task_id='Configurations_Rotator',
    depends_on_past=False,
    bash_command=t6a_command,
    dag=dag)


t2.set_upstream(t1)
t3a.set_upstream(t2)
t4a.set_upstream(t3a)
t5a.set_upstream(t4a)
t3b.set_upstream(t2)
t4b.set_upstream([t6b, t4c])
t4c.set_upstream(t3b)
t6b.set_upstream(t3b)
t5b.set_upstream(t4b)
t6a.set_upstream(t5b)

