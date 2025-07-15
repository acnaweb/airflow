from operators.api_to_bq_operator import ApiToBigqueryOperator

if __name__ == "__main__":
    try:
        print("▶️ Teste: Criação dinâmica da tabela e inserção")

        op = ApiToBigqueryOperator(
            task_id="insert_dynamic_table",
            api_url="https://randomuser.me/api/?results=2",
            project_id="study-gcp-398200", 
            dataset_id="raw", 
            table_id="stg_random_users",
            gcp_conn_id="google_cloud_default",
        )

        op.execute(context={})
        print("✅ Teste finalizado com sucesso.\n")

    except Exception as e:
        print(f"❌ Erro no teste: {e}\n")
