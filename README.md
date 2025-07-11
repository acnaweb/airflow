# Airflow

## Pre-req

Docker & Docker Compose - https://docs.docker.com/compose/install/

## Airflow in Docker

https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

### Usage

#### Run Airflow

```
make install_airflow
make run
```

#### Dags

```
./dags
```

#### Web Interface

http://localhost:8080

* user: airflow 
* password: airflow

####  Sending requests to the REST API

```
ENDPOINT_URL="http://localhost:8080/"
curl -X GET  \
    --user "airflow:airflow" \
    "${ENDPOINT_URL}/api/v1/pools"
```    

### Uninstall

#### Remove all

```
make clean_up
```

## References

- https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
- https://sistemas-operacionais.github.io/docker/docker-compose.html
- https://brilliantprogrammer.medium.com/how-to-trigger-airflow-dag-using-rest-api-dd40e3f7a30d

