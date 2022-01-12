

# Run with python3 airflow_example.py
# No messages in terminal mean nothing awful happened



from datetime import datetime, timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator




# These args will get passed on to each operator (ie, each process). Store this as a dict
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}





with DAG(
    'airflow_example',    # params of DAG which can feed into each process
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:


	dag.doc_md = """
	This is a docstring to annotate the doc
	"""  # otherwise, type it like this



	t1 = BashOperator(        # execute command from bash shell
	    task_id='print_date',
	    bash_command='date',
	)

	t2 = BashOperator(
	    task_id='sleep',
	    depends_on_past=False,
	    bash_command='sleep 5',
	    retries=3,
	)

	### Uses jinja to make loops of bash commands
	templated_command = dedent(
    """
	{% for i in range(5) %}
	    echo "{{ ds }}"
	    echo "{{ macros.ds_add(ds, 7)}}"
	    echo "{{ params.my_param }}"
	{% endfor %}
	"""
	)

	t3 = BashOperator(
	    task_id='templated',
	    depends_on_past=False,
	    bash_command=templated_command,
	    params={'my_param': 'Parameter I passed in'},
	)




t1 >> [t2, t3]  # task 1 has to be done before the others are run





































