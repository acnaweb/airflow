import os
from gusty import create_dags

gusty_dags_dir = os.path.join(
  os.environ["AIRFLOW_HOME"], 
  "dags", 
  "gusty_dags")

create_dags(
    # provide the path to your gusty DAGs directory
    gusty_dags_dir,
    # provide the namespace for gusty to use
    globals(),
    # By default, gusty places a LatestOnlyOperator at the root of the DAG.
    # We can disable this behavior by setting latest_only=False
    latest_only=False
)