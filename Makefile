export AIRFLOW_UID=1000

# Local development
install:
	docker compose up airflow-init

run:
	docker compose up

down:
	docker compose down

clean:
	docker compose down --volumes --remove-orphans --rmi all	