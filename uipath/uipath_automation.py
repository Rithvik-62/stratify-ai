"""
STRATIFY — Decision Intelligence Platform
UiPath RPA Automation Engine & Gmail SMTP Sender (uipath_automation.py)

Simulates & executes real RPA workflow for report detection, archiving,
execution logging, and Gmail SMTP email distribution.
"""

import os
import sys
import glob
import shutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
load_dotenv(dotenv_path=ENV_PATH, override=True)

UIPATH_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(UIPATH_DIR)
REPORTS_DIR = os.path.join(ROOT_DIR, "reports")
ARCHIVE_DIR = os.path.join(REPORTS_DIR, "archive")
LOG_PATH = os.path.join(UIPATH_DIR, "uipath_execution_log.csv")

class StratifyUiPathAutomation:
    """RPA Workflow Automation Engine for Executive Reporting & Email Distribution."""

    def __init__(self):
        os.makedirs(ARCHIVE_DIR, exist_ok=True)
        self._initialize_log()

    def _initialize_log(self):
        """Initializes uipath_execution_log.csv if not present."""
        if not os.path.exists(LOG_PATH):
            df_log = pd.DataFrame(columns=[
                "TIMESTAMP",
                "WORKFLOW",
                "STATUS",
                "FILE",
                "ACTION"
            ])
            df_log.to_csv(LOG_PATH, index=False)

    def log_event(self, workflow_name, status, filename, action_desc):
        """Logs RPA automation step to execution audit file."""
        entry = {
            "TIMESTAMP": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "WORKFLOW": workflow_name,
            "STATUS": status,
            "FILE": filename,
            "ACTION": action_desc
        }
        df_entry = pd.DataFrame([entry])
        df_entry.to_csv(LOG_PATH, mode='a', header=False, index=False)
        print(f"[UiPath RPA] {workflow_name} | {status} | File: {filename} | Action: {action_desc}")

    def send_gmail_smtp_report(self, pdf_path):
        """Sends PDF report attachment via Gmail SMTP server."""
        load_dotenv(dotenv_path=ENV_PATH, override=True)
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USER", "").strip()
        smtp_pass = os.getenv("SMTP_PASSWORD", "").strip().replace(" ", "")
        recipient = os.getenv("RECIPIENT_EMAIL", smtp_user).strip()

        filename = os.path.basename(pdf_path)

        if not smtp_user or not smtp_pass or "your_gmail_app_password" in smtp_pass:
            action_desc = "MANUAL ACTION REQUIRED — Please set valid Gmail SMTP_USER and SMTP_PASSWORD in .env file"
            self.log_event("STRATIFY_EMAIL_DISPATCH", "MANUAL_REQUIRED", filename, action_desc)
            return False, action_desc

        try:
            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = recipient
            msg['Subject'] = f"STRATIFY Executive Business Intelligence Report — {datetime.now().strftime('%B %d, %Y')}"

            body = (
                f"Hello Executive Team,\n\n"
                f"Please find attached the latest STRATIFY Executive Business Intelligence Report compiled from Snowflake DWH.\n\n"
                f"Report File: {filename}\n"
                f"Generated At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"Best regards,\n"
                f"STRATIFY Decision Intelligence Platform Engine"
            )
            msg.attach(MIMEText(body, 'plain'))

            with open(pdf_path, "rb") as f:
                attach = MIMEApplication(f.read(), _subtype="pdf")
                attach.add_header('Content-Disposition', 'attachment', filename=filename)
                msg.attach(attach)

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, recipient, msg.as_string())
            server.quit()

            action_desc = f"Successfully sent PDF report via Gmail SMTP to {recipient}"
            self.log_event("STRATIFY_EMAIL_DISPATCH", "EMAIL_SENT", filename, action_desc)
            return True, action_desc

        except Exception as e:
            err_msg = f"Gmail SMTP dispatch error: {str(e)}"
            self.log_event("STRATIFY_EMAIL_DISPATCH", "ERROR", filename, err_msg)
            return False, err_msg

    def run_report_archival_workflow(self):
        """Workflow: Detects new Executive PDF reports, archives previous reports, and dispatches via Gmail SMTP."""
        workflow_name = "STRATIFY_REPORT_AUTOMATION"
        
        pdf_files = sorted(glob.glob(os.path.join(REPORTS_DIR, "STRATIFY_Executive_*.pdf")))
        if not pdf_files:
            self.log_event(workflow_name, "IDLE", "N/A", "No new executive PDF report detected in reports/")
            return False

        latest_pdf = pdf_files[-1]
        latest_filename = os.path.basename(latest_pdf)

        self.log_event(workflow_name, "SUCCESS", latest_filename, "Detected new executive PDF report")

        # Archive older reports if more than 1 exists
        older_reports = pdf_files[:-1]
        for old_file in older_reports:
            old_name = os.path.basename(old_file)
            archive_dest = os.path.join(ARCHIVE_DIR, old_name)
            shutil.move(old_file, archive_dest)
            self.log_event(workflow_name, "ARCHIVED", old_name, f"Moved older report to reports/archive/{old_name}")

        # Execute Gmail SMTP Email Dispatch
        self.send_gmail_smtp_report(latest_pdf)
        return True

def main():
    rpa = StratifyUiPathAutomation()
    rpa.run_report_archival_workflow()

if __name__ == "__main__":
    main()
