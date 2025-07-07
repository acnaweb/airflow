#!/bin/bash

# Caminho para o arquivo de saída
OUTPUT_FILE="/opt/airflow/dags/dsa-p1-saida-capitalized.txt"

# Caminho para o banco de dados SQLite
DATABASE="/opt/airflow/dags/dsa_p1.db"

# Comando SQL para criar a tabela se ela não existir
SQL_CREATE="CREATE TABLE IF NOT EXISTS dsa_p1_dados (TIMESTAMP TEXT, VISITORID TEXT);"

# Cria a tabela no banco de dados (o banco de dados é criado se não existir)
sqlite3 $DATABASE "$SQL_CREATE"

# Importa o arquivo txt e carrega os dados na tabela
sqlite3 $DATABASE <<EOF
.mode tabs
.separator "#"
.import $OUTPUT_FILE dsa_p1_dados
EOF
