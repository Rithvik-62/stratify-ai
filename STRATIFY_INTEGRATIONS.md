# STRATIFY — Integration Matrix & Connection Audit

This document maintains the official connection status matrix across all tools in the STRATIFY platform.

---

## Connection Matrix

| Tool / Component | Integration Type | Status | Execution / Trigger Method | Manual Action Required |
| :--- | :--- | :--- | :--- | :--- |
| **Transaction Generator** | Local File Simulation | **Connected** | `python realtime/generator.py` | None |
| **Alteryx Designer** | Desktop Workflow (.yxmd) | **Manual Guide** | Alteryx Designer GUI Run | Open `alteryx/STRATIFY_Realtime_ETL.yxmd` & run batch |
| **Snowflake DWH** | Cloud SQL Connector | **Connected** | Direct DB Connection (`JQOFPHS-OZ81390`) | Credentials in `.env` |
| **Python Analytics** | Python DWH Queries | **Connected** | `database/queries.py` | None |
| **STRATIFY Dashboard** | Streamlit & Plotly UI | **Connected** | `python -m streamlit run app.py` | None |
| **UiPath RPA** | RPA File Automation | **Connected** | `python uipath/uipath_automation.py` | Archival automated |
| **Email Distribution** | SMTP Transport | **Manual / Optional** | `uipath/uipath_automation.py` | Set `SMTP_USER` / `SMTP_PASSWORD` in `.env` |
| **DeepSeek AI** | REST API | **Optional / Live** | `ai/deepseek_insights.py` | Set `DEEPSEEK_API_KEY` in `.env` |

---

## Manual Tool Guidelines

### Alteryx Manual Workflow Steps
1. Open **Alteryx Designer**.
2. File $\rightarrow$ Open Workflow $\rightarrow$ `d:\stratify-ai\alteryx\STRATIFY_Realtime_ETL.yxmd`.
3. Verify Input directory is set to `d:\stratify-ai\realtime\incoming\`.
4. Verify Output directory is set to `d:\stratify-ai\realtime\cleaned\`.
5. Click **Run** (Ctrl + R).
