"""
STRATIFY — Master Auto-Pilot Pipeline Orchestrator (run_master_pipeline.py)

Automates the complete 4-Tool Enterprise Business Intelligence Pipeline:
1. Tool 1 (Raw POS Batch Feed): Generates POS raw transaction data.
2. Tool 1 & 2 (Alteryx & Snowflake ETL): Cleans data and loads into Snowflake DWH.
3. Tool 3 (DeepSeek AI Engine): Synthesizes executive decision intelligence & ratios.
4. Tool 4 (UiPath RPA & Gmail SMTP): Compiles 8-page PDF & sends email via Gmail SMTP.
"""

import os
import sys
import time
from datetime import datetime

# Import internal module runners directly
from realtime.generator import RetailTransactionSimulator
from realtime.pipeline import StratifyRealtimePipeline
from reports.generate_pdf_report import generate_executive_report
from uipath.uipath_automation import StratifyUiPathAutomation

def run_master_automated_pipeline():
    """Executes the full 4-tool pipeline end-to-end automatically."""
    print("============================================================")
    print("⚡ STRATIFY — AUTOMATED 4-TOOL ENTERPRISE BI PIPELINE RUNNER")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("============================================================\n")

    # Step 1: Raw Data Generation
    print("[1/4] Generating Raw POS Business Transaction Batch...")
    simulator = RetailTransactionSimulator()
    batch_file, df_batch = simulator.generate_batch(count=1)
    print(f"  ✓ Raw Batch File Created: {batch_file}\n")
    time.sleep(1)

    # Step 2: Alteryx ETL & Snowflake DWH Ingestion (Tool 1 & 2)
    print("[2/4] Running Alteryx ETL Data Cleansing & Snowflake Ingestion...")
    pipeline = StratifyRealtimePipeline()
    proc_cnt = pipeline.run_pipeline(poll=False)
    print(f"  ✓ Alteryx ETL & Snowflake Ingestion Complete! ({proc_cnt} file(s) processed)\n")
    time.sleep(1)

    # Step 3: Executive PDF Report Compilation
    print("[3/4] Compiling 8-Page Executive Business Review PDF Report...")
    pdf_path = generate_executive_report()
    print(f"  ✓ PDF Report Compiled: {pdf_path}\n")
    time.sleep(1)

    # Step 4: UiPath RPA Archival & Gmail SMTP Email Dispatch (Tool 4)
    print("[4/4] Executing UiPath RPA Archival & Gmail SMTP Email Dispatch...")
    rpa = StratifyUiPathAutomation()
    rpa.run_report_archival_workflow()
    print("  ✓ UiPath RPA Workflow & Email Delivery Complete!\n")

    print("============================================================")
    print("🎉 FULL PIPELINE COMPLETED AUTOMATICALLY — ALL 4 TOOLS UPDATED!")
    print("============================================================\n")
    return True

if __name__ == "__main__":
    run_master_automated_pipeline()
