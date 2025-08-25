export AIRFLOW_UID=1000

install_airflow:
	docker compose up airflow-init --build
up:
	docker compose up -d --build

down:
	docker compose down	

clean:
	docker compose down --volumes --remove-orphans --rmi all
	
validate_imports:
	docker compose exec airflow-worker airflow dags list-import-errors

set_variables:
	docker compose up airflow-cli

test_conn_gcp:
	docker compose exec airflow-worker airflow connections test gcp
