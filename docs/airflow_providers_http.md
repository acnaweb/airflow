# Apache Airflow Providers HTTP - Principais Operators, Hooks e Sensors

## 📊 Tabela por Serviço

O provider **apache-airflow-proproviders-http** oferece integração genérica com APIs e serviços HTTP, permitindo chamadas REST e monitoramento de endpoints.

| Categoria | Operators | Hooks | Sensors |
|-----------|-----------|-------|---------|
| **HTTP Genérico** | `SimpleHttpOperator` | `HttpHook` | `HttpSensor` |

---

## ✅ Observações
- É um provider **genérico** para integração HTTP, usado como base para DAGs que consomem ou publicam em APIs REST.
- **`SimpleHttpOperator`** permite executar requisições HTTP (GET, POST, PUT, DELETE etc.).
- **`HttpHook`** gerencia conexões HTTP, autenticação (Basic Auth, headers, etc.) e execução de requests.
- **`HttpSensor`** permite monitorar endpoints até que uma condição seja atendida (ex.: esperar que um serviço retorne 200 OK).
- Muitos providers específicos (ex.: Slack, Google, Datadog) usam internamente esse provider HTTP.