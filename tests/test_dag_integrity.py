# import os
# import pytest
# from airflow.models import DagBag

# DAGS_PATH = os.path.join(os.path.dirname(__file__), "..", "dags")

# @pytest.fixture(scope="module")
# def dag_bag():
#     return DagBag(dag_folder=DAGS_PATH, include_examples=False)

# def test_dag_import(dag_bag):
#     assert len(dag_bag.dags) > 0, "Nenhuma DAG foi carregada"
#     assert len(dag_bag.import_errors) == 0, f"Erros de importação: {dag_bag.import_errors}"
