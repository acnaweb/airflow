# Boas Práticas para Nomenclatura de Pipelines (Airflow + Gusty)

> **Contexto**: O Gusty usa **o nome da pasta como `dag_id`**. Este guia padroniza como nomear pipelines (DAGs) **sem incluir o ambiente** no `dag_id`. A separação por ambiente deve ser feita pelo **processo de deploy/loader** e por **tags**.

---

## 🎯 Objetivos
- `dag_id` curto, legível e **único dentro do projeto**.
- Não incluir `env` no `dag_id` (controle de ambiente via deploy/loader).
- Facilitar filtros e observabilidade pela UI usando **tags** consistentes.

---

## 1) Formato do `dag_id` (== nome da pasta)
**Padrão (2 blocos):**
```
<project>__<pipeline>
```
- `project`: ID do projeto GCP (e.g., `study-gcp`, `prj-analytics-123`, `prj-risk-456`).
- `pipeline`: nome lógico do processo (e.g., `sales_daily`, `credit_scores_hourly`).

**Exemplos válidos**
- `study-gcp__sales_daily`
- `prj-analytics-123__customer_dedup_hourly`
- `prj-risk-456__credit_scores_training`

**Por quê?**
- Deixa o `dag_id` limpo e estável.
- Evita colisão entre pipelines dentro de um mesmo projeto.
- O ambiente fica livre para ser trocado sem renomear DAGs.

---

## 2) Estilo e caracteres
- Use **minúsculas**, números, `_` e `-` (dentro de cada bloco).
- Separador de blocos: **duplo underscore `__`**.
- Evite espaços, acentos, maiúsculas, PII e segredos.

**Regex sugerida (lint):**
```
^[a-z0-9-]+__[a-z0-9_]+$
```

---

## 3) Nome da pasta = `dag_id`
- No Gusty, **o nome da pasta define o `dag_id`** — `METADATA.yml` não sobrescreve.
- Não renomeie pastas após ir para produção (perde histórico/metrics).

**Estrutura mínima**
```
dags/
└─ study-gcp__sales_daily/
    ├─ METADATA.yml
    ├─ 10_extract_*.yml
    ├─ 20_transform_*.yml
    ├─ 30_validate_*.yml
    └─ 40_load_*.yml
```

---

## 4) Como isolar ambientes (dev/stg/prod) sem `env` no nome
- **Loader por variável** (ex.: Variable `env`) que decide **quais DAGs carregar**.
- **Build seletivo** no CI/CD: publicar no `DAGS_FOLDER` somente as DAGs do ambiente alvo.
- **Tags** indicam o ambiente do deploy atual, mas **não** fazem parte do `dag_id`.

> Resultado: o mesmo repositório gera artefatos de deploy separados por ambiente **sem renomear** as DAGs.

---

## 5) Conexões e variáveis

- **Conexões**  
  - Prefira conexões nomeadas com o padrão:  
    ```
    google_cloud_default__<project>
    ```
    Ex.: `google_cloud_default__study-gcp`  
  - Isso garante que cada projeto tenha seu próprio escopo de autenticação, evitando colisões.

- **Variáveis do Airflow**  
  - Utilize variáveis **namespaced por projeto** no formato JSON.  
  - Chave no Airflow: `<project>`  
  - Exemplo de valor (JSON):  
    ```json
    {
      "raw_bucket": "gs://study-gcp-raw",
      "location": "us-central1",
      "bq_dataset": "raw_dataset"
    }
    ```
  - Acesso dentro das DAGs:  
    ```jinja
    {{ var.json.study-gcp.raw_bucket }}
    {{ var.json.study-gcp.bq_dataset }}
    ```

- **Boas práticas**  
  - Centralizar configs sensíveis (nomes de buckets, datasets, regiões) nas variáveis.  
  - Usar `params` apenas para parâmetros específicos da DAG (não para configs globais).  
  - Evitar hardcode em `task.yml` ou `task.py`.

---

## 6) Tags padrão (no `METADATA.yml`)
Use **sempre** as tags abaixo como padrão base:
```yaml
tags:
  - "project:study-gcp"  
  - "owner:produtos"
  - "domain:cdp"
  - "pii:false"
```
> Adicione outras tags técnicas quando fizer sentido (ex.: `tech:bq`, `tech:gcs`, `sla:30`).

---

## 7) Dicas para `<pipeline>`
- Indique periodicidade quando relevante: `*_daily`, `*_hourly`, `*_weekly`.
- Evite nomes genéricos: prefira `orders_ingestion` a `etl`.
- Mantenha consistência com nomes de tasks: `extract_*`, `transform_*`, `validate_*`, `load_*`, `notify_*`.

---

## 8) Do & Don’t
**Faça**
- `study-gcp__orders_daily`
- `prj-analytics-123__web_events_hourly`
- Tags padronizadas e variáveis/conexões por projeto

**Evite**
- `etl`, `main`, `pipeline1`
- Misturar maiúsculas/acentos
- Incluir `env` no `dag_id` quando o deploy já isola por ambiente

---

## ✅ Checklist rápido de revisão
- [ ] A pasta segue `^[a-z0-9-]+__[a-z0-9_]+$`?
- [ ] O `dag_id` não contém `env`?
- [ ] Tags incluem o bloco padrão?
- [ ] Variáveis/Conexões apontam para o **projeto correto**?
- [ ] `pipeline` é descritivo e consistente com tasks?