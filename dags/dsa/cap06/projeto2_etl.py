#!/usr/bin/env python
# coding: utf-8

# Importando bibliotecas necessárias
import os
import sqlite3
import requests
import datetime
import pandas as pd 

# Definição da função para extrair dados da API
def dsa_extrai_dados_api():

    # Obtendo a data e hora atual
    hoje = datetime.datetime.now()
    
    # Fazendo uma solicitação GET para a API do tempo (coloque aqui sua chave da API)
    dados_api = requests.get("http://api.weatherapi.com/v1/current.json?key=28dba66354454315bde00517241501&q=Rio de Janeiro&aqi=yes")
    
    # Convertendo a resposta da API em JSON
    dsa_dados = dados_api.json()

    # Criando um dicionário a partir dos dados JSON
    dicionario_dados = {
        "temperature": [dsa_dados["current"]["temp_c"]],
        "wind_speed": [dsa_dados["current"]["wind_kph"]],
        "condition": [dsa_dados["current"]["condition"]["text"]],
        "precipitation": [dsa_dados["current"]["precip_mm"]],
        "humidity": [dsa_dados["current"]["humidity"]],
        "feels_like_temp": [dsa_dados["current"]["feelslike_c"]],
        "pressure": [dsa_dados["current"]["pressure_mb"]],
        "visibility": [dsa_dados["current"]["vis_km"]],
        "is_day": [dsa_dados["current"]["is_day"]],
        "timestamp": [hoje]
    }

    # Convertendo o dicionário em um DataFrame do Pandas
    return pd.DataFrame(dicionario_dados)

# Definição da função para verificar a qualidade dos dados
def dsa_data_quality(dsa_df_dados):
    
    # Verifica se o DataFrame está vazio
    if dsa_df_dados.empty:
        print("Os dados não foram extraídos")
        return False
    
    # Verifica se há valores nulos no DataFrame
    if dsa_df_dados.isnull().values.any():
        print("Valores ausentes detectados. Tratamento dos dados será necessário.")

# Definição da função para transformar os dados
def dsa_transforma_dados(dsa_df_dados):
    
    # Convertendo a coluna 'is_day' para tipo booleano
    dsa_df_dados["is_day"] = dsa_df_dados["is_day"].astype(bool)
    
    # Criando uma nova coluna 'ID' combinando 'timestamp' e 'temperature'
    dsa_df_dados["ID"] = dsa_df_dados['timestamp'].astype(str) + "-" + dsa_df_dados["temperature"].astype(str)
    
    return dsa_df_dados

# Definição da função para realizar a extração e transformação dos dados
def dsa_extrai_transforma():
    
    # Chamando a função de extração de dados da API
    dsa_df_dados = dsa_extrai_dados_api()
    
    # Chamando a função de transformação dos dados
    dsa_df_dados = dsa_transforma_dados(dsa_df_dados)

    # Chamando a função de verificação da qualidade dos dados
    dsa_data_quality(dsa_df_dados)
    
    return dsa_df_dados

# Definição da função principal para realizar o processo ETL
def dsa_processo_etl():
    
    # Chamando a função de extração e transformação dos dados
    df = dsa_extrai_transforma()
    
    # Definindo o caminho do arquivo CSV
    file_path = "/opt/airflow/dags/projeto2_dados.csv"
    
    # Verifica se o arquivo CSV já existe para decidir se inclui o cabeçalho
    header = not os.path.isfile(file_path)
    
    # Salvando o DataFrame no arquivo CSV no modo append
    df.to_csv(file_path, mode='a', index=False, header=header)

    # Conectando ao banco de dados SQLite (isso criará o arquivo de banco de dados se ele não existir)
    conn = sqlite3.connect('/opt/airflow/dags/projeto2_database.db')

    # Salvando o DataFrame no banco de dados SQLite
    df.to_sql('projeto2_tabela', conn, if_exists='append', index=False)

    # Fechando a conexão com o banco de dados
    conn.close()


