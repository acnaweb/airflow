#!/bin/bash
# A linha acima é o shebang, que indica que este script deve ser executado em um shell bash.

# Imprime a string "dsa-etl" no terminal.
echo "dsa-etl"

# Usa o comando cut para extrair as colunas 1 e 4 do arquivo dsa-p1-entrada.txt localizado em /opt/airflow/dags, 
# delimitadas por '#', e redireciona a saída para dsa-p1-saida.txt no mesmo diretório.
cut -f1,4 -d"#" /opt/airflow/dags/dsa-p1-entrada.txt > /opt/airflow/dags/dsa-p1-saida.txt

# Utiliza o comando tr para converter todas as letras minúsculas em maiúsculas 
# do conteúdo de dsa-p1-saida.txt e redireciona a saída para dsa-p1-saida-capitalized.txt no mesmo diretório.
tr "[a-z]" "[A-Z]" < /opt/airflow/dags/dsa-p1-saida.txt > /opt/airflow/dags/dsa-p1-saida-capitalized.txt

# Empacota e comprime o arquivo dsa-p1-saida-capitalized.txt em um arquivo tar.gz chamado dsa-p1-log.tar.gz,
# armazenando no diretório /opt/airflow/dags.
tar -czvf /opt/airflow/dags/dsa-p1-log.tar.gz /opt/airflow/dags/dsa-p1-saida-capitalized.txt
