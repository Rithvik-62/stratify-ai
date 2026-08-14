# STRATIFY — Setup & Configuration Guide

## Environment Prerequisites

- **Python 3.10+**
- **Snowflake Data Warehouse Account**
- **ReportLab** (`pip install reportlab`)
- **Streamlit & Plotly** (`pip install streamlit plotly pandas numpy snowflake-connector-python python-dotenv`)

---

## Environment Variables (`.env`)

Create or modify `.env` in the root workspace directory:

```ini
# Snowflake DWH Configuration
SNOWFLAKE_ACCOUNT=JQOFPHS-OZ81390
SNOWFLAKE_USER=RIXS
SNOWFLAKE_PASSWORD=Riansalian@001
SNOWFLAKE_DATABASE=NOVAKART_DB
SNOWFLAKE_SCHEMA=ANALYTICS
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_ROLE=ACCOUNTADMIN

# Optional AI & Email Configurations
DEEPSEEK_API_KEY=your_deepseek_api_key_here
SMTP_USER=executive_reports@company.com
SMTP_PASSWORD=your_email_app_password
```

---

## Deployment & Execution Steps

### 1. Launch Executive Dashboard
```bash
python -m streamlit run app.py
```

### 2. Run Real-Time Transaction Generator
```bash
python realtime/generator.py --mode single --count 1
```

### 3. Run Ingestion Pipeline Engine
```bash
python realtime/pipeline.py
```

### 4. Execute UiPath RPA Reporting Automation
```bash
python uipath/uipath_automation.py
```
