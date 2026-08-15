# STRATIFY — Public Deployment Guide (GitHub + Streamlit Cloud)

## 📋 Quick Summary

**STRATIFY** is a real-time decision intelligence dashboard that:
- Connects to Snowflake data warehouse
- Displays live KPIs, RFM analysis, and customer insights
- Generates PDF executive reports
- Sends reports via email automation
- Runs on Streamlit with full AI/ML capabilities

---

## 🚀 Deploy to Streamlit Cloud (Recommended for Teachers/Demos)

### Step 1: Prepare Your Local Repo for GitHub

```bash
# Navigate to the project
cd stratify-ai

# Stage only the safe files (source code, docs, config examples)
git add -A
git commit -m "Clean public deployment: source code + safe configs"

# Verify no secrets are staged
git status  # Should show only .py, .md, .yml, .txt, .toml, .yaml files

# Push to GitHub
git push origin main
```

### Step 2: Connect Snowflake + Email in Streamlit Cloud

1. Go to [streamlit.io](https://streamlit.io) and sign up with GitHub
2. Click **New App** → Select your `stratify-ai` repo → `main` branch → `app.py`
3. Click **Advanced Settings** → Add Secrets:

```toml
# Streamlit Cloud Secrets (.streamlit/secrets.toml)
SNOWFLAKE_ACCOUNT = "your_account_name"
SNOWFLAKE_USER = "your_username"
SNOWFLAKE_PASSWORD = "your_password"
SNOWFLAKE_DATABASE = "NOVAKART_DB"
SNOWFLAKE_SCHEMA = "ANALYTICS"
SNOWFLAKE_WAREHOUSE = "COMPUTE_WH"
SNOWFLAKE_ROLE = "ACCOUNTADMIN"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = "587"
SMTP_USER = "your_email@gmail.com"
SMTP_PASSWORD = "your_app_password"
RECIPIENT_EMAIL = "recipient@gmail.com"

DEEPSEEK_API_KEY = "your_key"  # Optional
SERPER_API_KEY = "your_key"    # Optional
```

4. Click **Deploy** and wait ~5 minutes
5. Share the public Streamlit Cloud URL with your teachers

---

## 🏠 Deploy Locally (for testing before cloud)

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
cp .env.example .env
# Edit .env with your real Snowflake & SMTP credentials

# Run the app
streamlit run app.py
```

Access: `http://localhost:8501`

---

## 🐳 Deploy with Docker (Optional, for VPS/Cloud Servers)

### Build Image
```bash
docker build -t stratify-ai .
```

### Run Container
```bash
docker run -p 8501:8501 \
  -e SNOWFLAKE_ACCOUNT=your_account \
  -e SNOWFLAKE_USER=your_user \
  -e SNOWFLAKE_PASSWORD=your_pass \
  -e SNOWFLAKE_DATABASE=NOVAKART_DB \
  -e SNOWFLAKE_SCHEMA=ANALYTICS \
  -e SNOWFLAKE_WAREHOUSE=COMPUTE_WH \
  -e SNOWFLAKE_ROLE=ACCOUNTADMIN \
  -e SMTP_SERVER=smtp.gmail.com \
  -e SMTP_PORT=587 \
  -e SMTP_USER=your_email@gmail.com \
  -e SMTP_PASSWORD=your_app_password \
  -e RECIPIENT_EMAIL=recipient@gmail.com \
  stratify-ai
```

---

## ✅ Pre-Deployment Checklist

- [ ] `.env` is in `.gitignore` (no secrets in repo)
- [ ] `.env.example` contains only placeholders
- [ ] Git repo is clean and only has source files
- [ ] Snowflake account is accessible and NOVAKART_DB exists
- [ ] Gmail app password is generated (not plain Gmail password)
- [ ] All dependencies in `requirements.txt` are up-to-date
- [ ] Local test: `streamlit run app.py` starts without errors
- [ ] Git remote points to GitHub: `git remote -v`

---

## 🔗 File Structure for Deployment

```
stratify-ai/
├── app.py                          # Main Streamlit app
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker build config
├── .env.example                    # Secret template (NEVER .env)
├── .gitignore                      # Excludes secrets
├── database/
│   ├── snowflake_connection.py    # DB connection logic
│   └── services.py                 # DB queries
├── components/                     # UI components
├── analytics/                      # Analytics logic
├── uipath/
│   └── uipath_automation.py        # Email automation
├── realtime/                       # Realtime data pipeline
├── reports/                        # PDF report generation
└── [documentation files]           # Setup guides
```

---

## 🔐 Security Checklist for Public Repo

✅ **What's included (safe to commit):**
- All `.py` source code
- UI components and analytics logic
- Dockerfile and docker-compose
- `.env.example` (placeholders only)
- `.gitignore` (protects real `.env`)
- Documentation and setup guides

❌ **What's NOT included (protected by .gitignore):**
- `.env` (real credentials)
- `*.log` files
- Generated CSVs and PDFs
- UiPath local cache files
- Python `__pycache__`

---

## 📞 Support

For questions:
1. Check [STRATIFY_SETUP.md](./STRATIFY_SETUP.md) for detailed setup
2. Review [STRATIFY_END_TO_END_GUIDE.md](./STRATIFY_END_TO_END_GUIDE.md) for full workflow
3. See [Snowflake integration status](./STRATIFY_INTEGRATION_STATUS.md)

---

**Ready to deploy? Push to GitHub and connect Streamlit Cloud in 3 minutes! 🚀**
