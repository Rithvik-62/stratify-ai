"""
STRATIFY — Retail Intelligence & Data Analytics Platform
Near-Real-Time Ingestion Pipeline Monitor (monitor.py)

Displays a console dashboard of pipeline execution metrics, file detection counts,
processed/rejected record totals, freshness, and current pipeline status.
"""

import os
import sys
import glob
import pandas as pd
from datetime import datetime

# Reconfigure stdout for UTF-8 support on Windows terminals
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Import configuration
try:
    from config import (
        INCOMING_DIR,
        PROCESSED_DIR,
        REJECTED_DIR,
        PROCESSING_LOG_PATH,
        STATUS_READY,
        STATUS_PROCESSING,
        STATUS_SUCCESS,
        STATUS_FAILED
    )
except ImportError:
    from realtime.config import (
        INCOMING_DIR,
        PROCESSED_DIR,
        REJECTED_DIR,
        PROCESSING_LOG_PATH,
        STATUS_READY,
        STATUS_PROCESSING,
        STATUS_SUCCESS,
        STATUS_FAILED
    )

def display_pipeline_monitor():
    """Calculates and displays real-time pipeline status dashboard."""
    incoming_files = glob.glob(os.path.join(INCOMING_DIR, "*.csv"))
    processed_files = glob.glob(os.path.join(PROCESSED_DIR, "*.csv"))
    rejected_files = glob.glob(os.path.join(REJECTED_DIR, "*.csv"))

    files_detected = len(incoming_files) + len(processed_files) + len(rejected_files)
    files_processed_cnt = len(processed_files) + len(rejected_files)

    rows_processed_tot = 0
    rows_rejected_tot = 0
    last_success_time = "N/A"
    last_error_msg = "None"
    current_status = STATUS_READY

    if len(incoming_files) > 0:
        current_status = STATUS_PROCESSING

    if os.path.exists(PROCESSING_LOG_PATH):
        try:
            df_log = pd.read_csv(PROCESSING_LOG_PATH)
            if not df_log.empty:
                rows_processed_tot = int(df_log["ROWS_PROCESSED"].sum())
                rows_rejected_tot = int(df_log["ROWS_REJECTED"].sum())

                # Get last successful load
                success_df = df_log[df_log["STATUS"] == "SUCCESS"]
                if not success_df.empty:
                    last_success_time = str(success_df.iloc[-1]["PROCESS_TIME"])
                    current_status = STATUS_SUCCESS

                # Get last error
                err_df = df_log[df_log["ERROR_MESSAGE"].notnull() & (df_log["ERROR_MESSAGE"] != "")]
                if not err_df.empty:
                    last_error_msg = str(err_df.iloc[-1]["ERROR_MESSAGE"])
                    if df_log.iloc[-1]["STATUS"] in ["FAILED", "REJECTED"]:
                        current_status = STATUS_FAILED
        except Exception as e:
            last_error_msg = str(e)

    print("\n" + "=" * 68)
    print("      STRATIFY — AUTOMATED PIPELINE MONITORING DASHBOARD")
    print("=" * 68)
    print(f" PIPELINE_STATUS        : {current_status}")
    print(f" FILES_DETECTED         : {files_detected} (Incoming: {len(incoming_files)})")
    print(f" FILES_PROCESSED        : {files_processed_cnt}")
    print(f" ROWS_PROCESSED         : {rows_processed_tot}")
    print(f" ROWS_REJECTED          : {rows_rejected_tot}")
    print(f" LAST_SUCCESSFUL_LOAD   : {last_success_time}")
    print(f" LAST_ERROR             : {last_error_msg}")
    print("=" * 68 + "\n")

if __name__ == "__main__":
    display_pipeline_monitor()
