export AIRFLOW_UID=1000

# Local development
install:
	python -m venv venv; \
	. venv/bin/activate; \
	pip install --upgrade pip; \
	pip install -r requirements.dev.txt; \
	pip install -r requirements.txt; \
	mkdir dags logs plugins tests dbt; \

build:
	docker compose build

run:
	docker compose up

down:
	docker compose down

clean:
	docker compose down --volumes --remove-orphans --rmi all	