# 🔄 ALTERYX WORKFLOW EXECUTION & MANUAL GATE GUIDE
**Project:** STRATIFY — Decision Intelligence Platform  
**Component:** Alteryx Designer Workflow ([`alteryx/Stratify_ETL(final).yxmd`](file:///d:/stratify-ai/alteryx/Stratify_ETL(final).yxmd))  
**Classification:** Near-real-time end-to-end BI pipeline with a manual Alteryx execution gate  

---

## 1. Why Manual Execution Is Required

Alteryx Designer is the authoritative data-engineering engine for the STRATIFY platform.

When testing CLI execution via `AlteryxEngineCmd.exe` on this machine (Version 2025.2.1.117), Alteryx returns:
```
Error - Alteryx Engine: The Feature "API or FlowChartMode" is not licensed.
```

In standalone desktop licenses of Alteryx Designer, headless command-line execution requires an enterprise Server/API add-on license. Therefore, the real-world workflow execution in Alteryx Designer is performed via the desktop GUI using **`Ctrl + R`**.

---

## 2. Directory Architecture

| Directory | Path | Purpose |
|---|---|---|
| **Raw Input** | `D:\stratify-ai\realtime\incoming\` | Receives raw POS transaction CSV files (`sales_batch_YYYYMMDD_HHMMSS.csv`) |
| **Alteryx Clean Output** | `D:\stratify-ai\realtime\processed_ready\` | Output destination for verified, clean micro-batches ready for Snowflake |
| **Quarantine / Rejections** | `D:\stratify-ai\realtime\rejected\` | Quarantines corrupted records (negative quantities, duplicate SALE_IDs, orphan keys) |
| **Historical Master Output**| `D:\stratify-ai\Output\` | Master datasets (`sales_clean.csv`, `customers_clean.csv`, etc.) |

---

## 3. Step-by-Step Execution in Alteryx Designer

1. Launch **Alteryx Designer**.
2. Open [`D:\stratify-ai\alteryx\Stratify_ETL(final).yxmd`](file:///d:/stratify-ai/alteryx/Stratify_ETL(final).yxmd).
3. Verify that:
   - **Sales Input (ToolID 601)** points to `D:\stratify-ai\realtime\incoming\sales_batch_*.csv`.
   - **Select Tool (ToolID 602)** has `Unit_Price`, `Discount`, `Cost` set to `Double`, `Quantity` set to `Int32`, `Date` set to `Date`.
   - **Clean Output (ToolID 608)** points to `D:\stratify-ai\realtime\processed_ready\sales_clean.csv`.
4. Press **`Ctrl + R` (Run)**.
5. Once complete, Alteryx writes the validated batch to `realtime/processed_ready/`.
6. STRATIFY's Snowflake ingestion engine (`realtime/pipeline.py`) automatically ingests the validated batch into Snowflake `NOVAKART_DB.ANALYTICS.RAW_SALES`.
