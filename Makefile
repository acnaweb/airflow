export AIRFLOW_UID=1000

install:
	python -m venv venv; \
	. venv/bin/activate; \
	pip install --upgrade pip setuptools wheel; \
	pip install pre-commit; \
	pip install -e .[dev,quality]; \
	pre-commit install; \
	git config --bool flake8.strict true; \
	mkdir -p ./logs ./plugins ./config; \

install_airflow:
	docker compose up airflow-init --build

quality:
	black dags
	isort dags
	flake8 dags

test:
	pytest

run:
	docker compose up -d --build

down:
	docker compose down	

clean:
	docker compose down --volumes --remove-orphans --rmi all
	
validate_imports:
	docker compose exec airflow-worker airflow dags list-import-errors

test_conn_gcp:
	docker compose exec airflow-worker airflow connections test gcp
