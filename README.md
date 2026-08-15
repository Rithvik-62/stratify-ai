# 🎯 STRATIFY — AI-Powered Decision Intelligence Platform

A real-time business analytics and automation platform built on **Streamlit** + **Snowflake** + **Python**, designed for executive decision-making and intelligent data-driven insights.

---

## ✨ Key Features

### 📊 **Real-Time Analytics Dashboard**
- Live KPI tracking and trend analysis
- Customer segmentation (RFM Analysis)
- Sales forecasting with AI
- Data quality monitoring
- Interactive visualizations with Plotly

### 🤖 **AI-Powered Insights**
- DeepSeek API integration for intelligent analysis
- Natural language processing for business insights
- Scenario simulation and what-if analysis
- Automated pattern recognition

### 📧 **Intelligent Automation**
- Automated PDF report generation
- Gmail SMTP email distribution
- Report archival and logging
- UiPath integration for RPA workflows

### 🔄 **Real-Time Data Pipeline**
- Automated data ingestion from multiple sources
- Live transaction processing
- Snowflake data warehouse integration
- Data validation and quality checks

### 🏠 **Multi-Tenant Architecture**
- Customer, product, and employee management
- Sales and inventory tracking
- Finance and profitability analysis
- Hierarchical data organization

---

## 🚀 Quick Start

### Option 1: Run Locally (5 minutes)

```bash
# Clone the repo
git clone https://github.com/Rithvik-62/stratify-ai.git
cd stratify-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your credentials
cp .env.example .env
# Edit .env with your Snowflake and Gmail credentials

# Run the dashboard
streamlit run app.py
```

**Access:** http://localhost:8501

### Option 2: Deploy to Streamlit Cloud (Free, Recommended)

1. Push this repo to GitHub
2. Go to [streamlit.io](https://streamlit.io) and sign up
3. Click **New App** → Select `stratify-ai` repo → `main` → `app.py`
4. Add secrets in **Advanced Settings** (see `.streamlit/secrets.toml.example`)
5. Click **Deploy** and share the public link with your team!

See [DEPLOYMENT_GUIDE_PUBLIC.md](./DEPLOYMENT_GUIDE_PUBLIC.md) for detailed instructions.

---

## 📋 Prerequisites

### Required Credentials
- **Snowflake Account** (JQOFPHS-OZ81390 or your own account)
  - Database: `NOVAKART_DB`
  - Schema: `ANALYTICS`
  - Warehouse: `COMPUTE_WH`

- **Gmail SMTP** (for email reports)
  - Gmail address
  - [Generate app password](https://support.google.com/accounts/answer/185833) (not regular password)

- **API Keys** (Optional)
  - DeepSeek API key
  - Serper.dev API key

### System Requirements
- Python 3.8+
- 4GB RAM minimum
- Internet connection for Snowflake/API access

---

## 📂 Project Structure

```
stratify-ai/
├── app.py                          # Main Streamlit dashboard
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker configuration
├── .env.example                    # Environment template
├── .gitignore                      # Git security rules
│
├── database/                       # Data layer
│   ├── snowflake_connection.py     # Snowflake connector
│   ├── queries.py                  # SQL queries
│   └── services.py                 # Database services
│
├── components/                     # UI components
│   ├── header.py                   # Dashboard header
│   ├── kpi_cards.py                # KPI display
│   ├── charts.py                   # Chart components
│   ├── rfm_analysis.py             # RFM segmentation
│   ├── forecasting.py              # Forecasting UI
│   ├── pipeline_visualizer.py      # Pipeline status
│   ├── health_score.py             # Health metrics
│   └── transaction_feed.py         # Live transaction feed
│
├── analytics/                      # Business logic
│   └── services.py                 # Analytics calculations
│
├── uipath/                         # Automation workflows
│   ├── uipath_automation.py        # Email/report automation
│   └── STRATIFY_REPORT_AUTOMATION.xaml  # UiPath demo workflow
│
├── realtime/                       # Real-time pipeline
│   ├── config.py                   # Pipeline config
│   ├── generator.py                # Data generator
│   ├── pipeline.py                 # Data processing
│   └── README.md                   # Pipeline docs
│
├── reports/                        # Report generation
│   └── generate_pdf_report.py      # PDF report builder
│
├── snowflake/                      # SQL schemas
│   └── [*.sql]                     # Database setup scripts
│
└── [Documentation]                 # Guides and specs
    ├── STRATIFY_SETUP.md
    ├── STRATIFY_END_TO_END_GUIDE.md
    ├── STRATIFY_ARCHITECTURE.md
    └── DEPLOYMENT_GUIDE_PUBLIC.md
```

---

## 🔧 Configuration

### Environment Variables (`.env`)

```env
# Snowflake Connection
SNOWFLAKE_ACCOUNT=your_account_name
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_DATABASE=NOVAKART_DB
SNOWFLAKE_SCHEMA=ANALYTICS
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_ROLE=ACCOUNTADMIN

# Gmail SMTP (for report distribution)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
RECIPIENT_EMAIL=recipient@gmail.com

# Optional AI APIs
DEEPSEEK_API_KEY=your_key
SERPER_API_KEY=your_key
```

**⚠️ IMPORTANT:** Never commit `.env` to GitHub. Use `.env.example` as a template.

---

## 🏗️ Architecture

### Data Flow
```
Snowflake Data Warehouse
    ↓
Database Connection (snowflake_connection.py)
    ↓
Real-Time Pipeline (realtime/pipeline.py)
    ↓
Analytics Services (analytics/services.py)
    ↓
Streamlit Dashboard (app.py)
    ↓
UI Components + Charts
    ↓
User Browser (Live Streaming)
```

### Automation Flow
```
Dashboard Report Generation
    ↓
PDF Archive (reports/generate_pdf_report.py)
    ↓
UiPath Automation Trigger (uipath/uipath_automation.py)
    ↓
Gmail SMTP Distribution
    ↓
Email Inbox
```

---

## 📊 Dashboard Tabs

1. **Executive Summary** - KPIs and key metrics
2. **Customer Analytics** - RFM segmentation and insights
3. **Sales Forecasting** - ML-based sales predictions
4. **Inventory & Finance** - Stock levels and profitability
5. **Live Transaction Feed** - Real-time transaction monitor
6. **Data Quality** - Data validation and health checks
7. **AI Insights** - DeepSeek-powered business insights
8. **Admin Panel** - System status and configuration
9. **Report Center** - PDF generation and archival

---

## 🤖 AI Integration

- **DeepSeek API**: Provides intelligent business insights
- **Natural Language**: Accepts business questions and returns analysis
- **Automated Recommendations**: Suggests actions based on data patterns

---

## ⚙️ Running in Production

### Streamlit Cloud (Recommended)
See [DEPLOYMENT_GUIDE_PUBLIC.md](./DEPLOYMENT_GUIDE_PUBLIC.md)

### Docker
```bash
docker build -t stratify-ai .
docker run -p 8501:8501 \
  -e SNOWFLAKE_ACCOUNT=your_account \
  -e SNOWFLAKE_USER=your_user \
  -e SNOWFLAKE_PASSWORD=your_pass \
  stratify-ai
```

### Manual Server
```bash
pip install -r requirements.txt
streamlit run app.py --server.port 8501
```

---

## 📖 Documentation

- [Setup Guide](./STRATIFY_SETUP.md) - Detailed setup instructions
- [End-to-End Guide](./STRATIFY_END_TO_END_GUIDE.md) - Full workflow walkthrough
- [Architecture](./STRATIFY_ARCHITECTURE.md) - System design and components
- [Integration Status](./STRATIFY_INTEGRATION_STATUS.md) - Verified integrations
- [Deployment Guide](./DEPLOYMENT_GUIDE_PUBLIC.md) - Cloud deployment steps
- [Limitations](./STRATIFY_LIMITATIONS.md) - Known constraints

---

## 🔐 Security

✅ **Best Practices Implemented:**
- Secrets managed via environment variables only
- No credentials in source code
- `.env` excluded from Git
- Snowflake connection pooling for safety
- Email passwords never logged

⚠️ **Before Deployment:**
- [ ] Change all default credentials
- [ ] Use app passwords, not plain passwords
- [ ] Enable Snowflake IP whitelisting
- [ ] Set secure environment variables on host

---

## 🐛 Troubleshooting

### Snowflake Connection Error
```
Error: Invalid credentials
→ Check SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD in .env
→ Verify Snowflake account is active and accessible
```

### Gmail SMTP Error
```
Error: Authentication failed
→ Use Gmail app password, not regular password
→ Enable "Less secure app access" if using business Gmail
→ Check SMTP_USER and SMTP_PASSWORD are correct
```

### Dashboard Not Loading
```
Error: Connection timeout
→ Check internet connection
→ Verify Snowflake warehouse is running
→ Check if NOVAKART_DB exists in Snowflake
```

For more help, see the full [setup documentation](./STRATIFY_SETUP.md).

---

## 📞 Support & Contributions

For issues, questions, or contributions:
1. Check existing documentation files
2. Review the [Architecture guide](./STRATIFY_ARCHITECTURE.md)
3. Test locally with sample data before deploying

---

## 📄 License

This project is provided as-is for educational and business intelligence purposes.

---

## 🎓 Educational Use

This project is designed for:
- Data science and business analytics courses
- Snowflake and cloud data warehouse training
- Python Streamlit dashboard development
- Real-world business automation scenarios

Perfect for **teacher demonstrations** and **student portfolio projects**! 🎉

---

**Made with ❤️ for intelligent business decisions**

**Ready to deploy?** → See [DEPLOYMENT_GUIDE_PUBLIC.md](./DEPLOYMENT_GUIDE_PUBLIC.md) for step-by-step instructions.
