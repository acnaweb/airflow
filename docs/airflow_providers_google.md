# Apache Airflow Providers Google - Principais Operators, Hooks e Sensors

## 📊 Tabela por Serviço

| Serviço | Operators | Hooks | Sensors |
|---------|-----------|-------|---------|
| **BigQuery** | `BigQueryInsertJobOperator`, `BigQueryExecuteQueryOperator`, `BigQueryCreateEmptyTableOperator`, `BigQueryDeleteTableOperator`, `BigQueryCheckOperator`, `BigQueryToGCSOperator`, `GCSToBigQueryOperator` | `BigQueryHook` | `BigQueryTableExistenceSensor`, `BigQueryTablePartitionExistenceSensor`, `BigQueryJobSensor` |
| **Cloud Storage (GCS)** | `GCSToGCSOperator`, `GCSToLocalOperator`, `LocalFilesystemToGCSOperator`, `GCSCreateBucketOperator`, `GCSDeleteBucketOperator` | `GCSHook` | `GCSObjectExistenceSensor`, `GCSObjectsWithPrefixExistenceSensor`, `GCSUploadSessionCompleteSensor` |
| **Dataproc** | `DataprocSubmitJobOperator`, `DataprocCreateClusterOperator`, `DataprocDeleteClusterOperator`, `DataprocScaleClusterOperator` | `DataprocHook` | `DataprocJobSensor`, `DataprocClusterScaleSensor` |
| **Dataflow** | `DataflowCreatePythonJobOperator`, `DataflowCreateJavaJobOperator`, `DataflowTemplatedJobStartOperator` | `DataflowHook` | `DataflowJobSensor` |
| **Pub/Sub** | `PubSubPublishMessageOperator`, `PubSubCreateTopicOperator`, `PubSubDeleteTopicOperator`, `PubSubCreateSubscriptionOperator` | `PubSubHook` | `PubSubPullSensor`, `PubSubTopicSensor` |
| **GKE (Kubernetes Engine)** | `GKEStartPodOperator`, `GKECreateClusterOperator`, `GKEDeleteClusterOperator` | `GKEHook` | `GKEClusterStateSensor` |
| **Cloud Functions** | `CloudFunctionsDeployFunctionOperator`, `CloudFunctionsDeleteFunctionOperator`, `CloudFunctionsInvokeFunctionOperator` | `CloudFunctionsHook` | — |
| **Cloud Run** | `CloudRunJobCreateOperator`, `CloudRunJobDeleteOperator`, `CloudRunJobExecuteOperator` | `CloudRunHook` | `CloudRunJobSensor` |
| **Vertex AI (AI Platform/AutoML)** | `AutoMLTrainModelOperator`, `AutoMLDeployModelOperator`, `VertexAIPredictionJobOperator`, `VertexAICreateDatasetOperator` | `VertexAIHook` | `VertexAIJobSensor` |
| **Composer (Airflow no GCP)** | `CloudComposerCreateEnvironmentOperator`, `CloudComposerDeleteEnvironmentOperator` | `CloudComposerHook` | `CloudComposerEnvironmentSensor` |
| **Firestore / Spanner / Bigtable** | `FirestoreExportDocumentsOperator`, `SpannerDeployInstanceOperator`, `BigtableCreateInstanceOperator` | `FirestoreHook`, `SpannerHook`, `BigtableHook` | — |
| **Drive / Sheets** | `GoogleDriveToGCSOperator`, `GoogleSheetsToGCSOperator`, `GCSToGoogleSheetsOperator` | `DriveHook`, `SheetsHook` | — |
| **Ads / Marketing** | `GoogleAdsListAccountsOperator`, `GoogleCampaignManagerReportRunOperator` | `GoogleAdsHook`, `GoogleCampaignManagerHook` | — |
| **Translate / Speech / Vision / Natural Language** | `CloudTranslateTextOperator`, `CloudSpeechToTextTranscribeOperator`, `CloudVisionDetectTextOperator`, `CloudNaturalLanguageAnalyzeEntitySentimentOperator` | `TranslateHook`, `SpeechToTextHook`, `VisionHook`, `NaturalLanguageHook` | — |

---

## ✅ Observações
- Essa lista cobre os **principais** recursos; o provider ainda inclui suporte a **Cloud SQL, Cloud Tasks, Memorystore, Secret Manager, DLP, Dataplex, Looker, AlloyDB** e outros.
- Todos seguem o mesmo padrão:
  - **Operator** → executa a ação.
  - **Hook** → autentica e conecta à API.
  - **Sensor** → espera por um estado.