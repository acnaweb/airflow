# Projeto 6 - Variáveis, Conexões e Sensores Para Extração e Movimentação de Dados com Airflow

# Import
import sqlite3

# Defina o caminho do banco de dados SQLite
db_path = "dsa.db"

# Conecte ao banco de dados (se não existir, ele será criado)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Crie a tabela vazia, se ela não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS weather_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    weather TEXT,
    temperature REAL,
    humidity INTEGER
)
""")

# Commit e fechar a conexão
conn.commit()
conn.close()

print(f"\nBanco de dados criado e tabela 'weather_data' está pronta em {db_path}")

print("\nObrigado DSA!\n")
