install:
	python -m venv venv; \
	. venv/bin/activate; \
	pip install --upgrade pip setuptools wheel; \
	pip install pre-commit; \
	pip install -e .[dev,quality]; \
	pre-commit install; \
	git config --bool flake8.strict true; \
	mkdir -p ./logs ./config; \

quality:
	black dags
	isort dags
	flake8 dags

test:
	pytest

validate_imports:
	docker compose exec airflow-worker airflow dags list-import-errors

set_variables:
	docker compose up airflow-cli

test_conn_gcp:
	docker compose exec airflow-worker airflow connections test gcp

