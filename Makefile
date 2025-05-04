export AIRFLOW_UID=1000

install:
	python -m venv venv; \
	. venv/bin/activate; \
	pip install --upgrade pip; \
	pip install pre-commit; \
	pip install -e .[dev]; \
	pre-commit install; \
	git config --bool flake8.strict true; \
	mkdir -p ./logs ./plugins ./config; \

install_airflow: install
	docker compose up airflow-init --build

formatter:
	black dags

typing: formatter
	mypy dags

lint: formatter
	flake8  dags

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
