export AIRFLOW_UID=1000

install:
	python -m venv venv; \
	. venv/bin/activate; \
	pip install --upgrade pip setuptools wheel; \
	pip install pre-commit; \
	pip install -e .[dev,quality]; \
	pre-commit install; \
	git config --bool flake8.strict true; \
	mkdir -p ./logs ./config; \

install_airflow:
	docker compose up airflow-init --build

quality:
	black dags
	isort dags
	flake8 dags

test:
	pytest

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

integrated_test:
	# python tests/integrated/test_api_to_gcs_operator.py
	python tests/integrated/test_api_to_bq_operator.py