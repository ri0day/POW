# -*- coding: UTF-8 -*-
"""
    dags.cmdb
    ~~~~~~~~~~~
"""
from datetime import timedelta
from airflow.utils import dates
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from tasks.vertex import Vertex
from tasks.edge import Edge

default_args = {
    'owner': "airflow",
    'depends_on_past': False,
    'start_date': dates.days_ago(1),
    'email': ["wumin@zillionfortune.com"],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG("aliyun",
          default_args=default_args,
          schedule_interval=timedelta(minutes=5))

v = Vertex()
e =  Edge()
vertex_task = PythonOperator(task_id="cmdb_vertex",
                             python_callable=v.main,
                             dag=dag)
edge_task = PythonOperator(task_id="cmdb_edge",
                           python_callable=e.main,
                           dag=dag)

vertex_task.set_downstream(edge_task)