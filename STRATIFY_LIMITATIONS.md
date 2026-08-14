# STRATIFY — System Architecture Boundaries & Limitations

## 1. Near-Real-Time Batch vs. True Event Streaming

- **Current Implementation:** Near-Real-Time Batch Processing (`sales_batch_*.csv` generated, staged to `@NOVAKART_STAGE`, and SQL MERGED into `RAW_SALES`).
- **Data Latency:** Typically 1 to 10 seconds per batch run.
- **Academic Distinction:** This is a batch-based micro-burst ingestion architecture. It is **not** an Apache Kafka / AWS Kinesis continuous event streaming pipeline.

---

## 2. Forecasting Data Requirements

- **Current Behavior:** If total historical transaction records $< 10$, Python analytics displays `"Forecast unavailable — insufficient historical data."`
- **Rationale:** Prevents misleading statistical trend lines when sample sizes are inadequate.

---

## 3. External Tool Manual Interfaces

- **Alteryx Designer:** GUI software execution must be triggered inside Alteryx Designer or via Alteryx Engine command-line (`AlteryxEngineCmd.exe`) if installed on Windows.
- **SMTP Email Distribution:** Requires explicit SMTP server authorization credentials to send emails over corporate mail servers.
