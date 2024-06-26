export AIRFLOW_UID=1000

# Local development
install:
	python -m venv venv; \
	. venv/bin/activate; \
	pip install --upgrade pip; \
	pip install -r requirements.dev.txt; \
	pip install -r requirements.dbt.txt; \
	pip install -r requirements.gcp.txt; \
	pip install -r requirements.oci.txt; \
	mkdir -p dags logs plugins tests dbt; \

run:
	docker compose up --build

down:
	docker compose down

clean:
	docker compose down --volumes --remove-orphans --rmi all	