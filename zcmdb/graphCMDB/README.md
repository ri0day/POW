### graphCMDB

##### 目录结构说明
- `aliyun`  
  - `__init__.py`
  - `base.py`  阿里云父类(供子类继承使用)
  - `ecs.py`  阿里云ECS
  - `nosql.py`  阿里云KV数据库 
  - `rds.py`  阿里云RDS
  - `slb.py`  阿里云负载均衡
  - `utils.py`  一些常用装饰器函数
  - `config.ini`  阿里云AccessKey
- `dags`  airflow DAGs目录
  - `cmdb.py`  创建CMDB DAG( Edge任务依赖于Vertex任务，先执行Vertex成功后才会执行Edge )
- `scripts`  初始化脚本存放目录
  - `init.py`  初始化脚本，创建database和collection
- `tasks`  airflow任务目录
  - `vertex.py`  同步节点(node or vertex)数据 
  - `edge.py`  同步关系(edge or relationship)数据
- `vendor`  阿里云PythonSDK补丁包
- `airflow.cfg`  airflow配置文件( **部署时注意修改相应参数** )
- `requirements.txt`  Python三方依赖包
- `tests`  

### 安装部署
1. `pip2.7 install -r requirements.txt` # 安装Python三方依赖，**使用Python2.7**
2. 安装Redis, MySQL, [ArangoDB数据库](https://www.arangodb.com/download-major/)
3. `export AIRFLOW_HOME=/path/to/project` # 设置airflow home到该项目的**绝对路径**，**一定要设置正确**, 否则airflow无法识别任务的路径
4. 修改`scripts/init.py`中的数据库相关信息(host, username, password)，运行该脚本创建初始数据库和相关集合
5. 修改`aliyun/config.ini`设置添加或修改正确的阿里云API Key
6. 修改`airflow.cfg`相关参数 
  * 替换所有'/Users/min/PycharmProjects'为`/path/to/project`目录
  * executor # 使用CeleryExecutor
  * sql_alchemy_conn # 指向MySQL数据库
  * broker_url # 指向Redis一个db
  * celery_result_backend # 指向Redis另一个db
7. 启动airflow
  * `airflow scheduler`
  * `airflow worker`
  * `airflow webserver` # 启动airflow WebUI，可选 

