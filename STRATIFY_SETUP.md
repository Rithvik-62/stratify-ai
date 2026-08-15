# ⚙️ STRATIFY — Complete Setup & Deployment Guide

## 1. Prerequisites

- Python 3.10+ (Recommended: Python 3.11)
- Snowflake Account with `ACCOUNTADMIN` or relevant database creation role
- Git & Virtual Environment

---

## 2. Quickstart Installation

```bash
# 1. Clone the repository
git clone https://github.com/Rithvik-62/stratify-ai.git
cd stratify-ai

# 2. Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 3. Install required Python packages
pip install -r requirements.txt
```

---

## 3. Environment Configuration

Copy `.env.example` to `.env` and fill in your real credentials:

```bash
cp .env.example .env
```

```ini
# Snowflake Data Warehouse Credentials
SNOWFLAKE_ACCOUNT=your_account_name
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_DATABASE=NOVAKART_DB
SNOWFLAKE_SCHEMA=ANALYTICS
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_ROLE=ACCOUNTADMIN

# DeepSeek AI API (Optional)
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Gmail SMTP Email Distribution
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password
RECIPIENT_EMAIL=your_recipient_email@gmail.com
```

---

## 4. Running STRATIFY Locally

```bash
# Launch the Streamlit Web Application
streamlit run app.py
```

Open your browser to: `http://localhost:8501`

---

## 5. Running the Master Pipeline Manually via CLI

To execute the 4-tool automated data pipeline via command line:

```bash
python run_master_pipeline.py
```

Pipeline sequence:
1. **POS Generator:** Creates a new batch in `realtime/incoming/`.
2. **Alteryx / Python ETL:** Cleans and validates the batch into `realtime/processed/`.
3. **Snowflake Ingestion:** Stages and MERGEs into `RAW_SALES`.
4. **DeepSeek AI Synthesis:** Analyzes live financial KPIs.
5. **Executive PDF Report:** Generates an 8-page review in `reports/`.
6. **UiPath RPA & Gmail:** Archives old reports and emails PDF to executives.
