# Apache Airflow Providers Common SQL - Principais Operators, Hooks e Sensors

## 📊 Tabela por Serviço

O provider **apache-airflow-providers-common-sql** oferece abstrações genéricas para trabalhar com bancos de dados relacionais usando SQL, servindo como base para outros providers (Postgres, MySQL, MSSQL, BigQuery etc.).

| Categoria | Operators | Hooks | Sensors |
|-----------|-----------|-------|---------|
| **SQL Genérico** | `SQLExecuteQueryOperator`, `SQLColumnCheckOperator`, `SQLTableCheckOperator`, `SQLIntervalCheckOperator`, `SQLCheckOperator`, `SQLValueCheckOperator`, `BranchSQLOperator` | `DbApiHook` (classe base), `SQLHook` | `SQLSensor`, `SQLTableExistenceSensor` |
| **Transferências** | `SQLToCSVOperator`, `SQLToGoogleSheetsOperator` (depende de outros providers) | — | — |
| **Checks e Qualidade de Dados** | `SQLCheckOperator`, `SQLValueCheckOperator`, `SQLIntervalCheckOperator`, `SQLColumnCheckOperator`, `SQLTableCheckOperator` | `SQLHook` | — |

---

## ✅ Observações
- Esse provider é **genérico**: implementa Operators, Hooks e Sensors baseados em **PEP-249 (DBAPI)**.
- Providers específicos (como `apache-airflow-providers-postgres`, `apache-airflow-providers-mysql`, `apache-airflow-providers-mssql`) herdam e estendem essas classes.
- Os principais usos são para **executar queries**, **verificar integridade dos dados** e **monitorar tabelas**.