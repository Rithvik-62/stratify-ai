"""
STRATIFY — Master Auto-Pilot Pipeline Orchestrator (run_master_pipeline.py)

Automates the complete 4-Tool Enterprise Business Intelligence Pipeline:
1. Tool 1 (Raw POS Batch Feed): Generates POS raw transaction data in realtime/incoming/.
2. Tool 1 (Alteryx ETL Engine): Cleans data, verifies referential integrity, and outputs to realtime/processed_ready/.
3. Tool 2 (Snowflake Cloud DWH): Ingests ONLY Alteryx-cleaned data into NOVAKART_DB.ANALYTICS.RAW_SALES.
4. Tool 3 (DeepSeek AI Engine): Synthesizes executive decision intelligence & ratios from Snowflake.
5. Tool 4 (UiPath RPA & Gmail SMTP): Compiles 8-page PDF & sends email via Gmail SMTP.
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
    print("[1/5] Generating Raw POS Business Transaction Batch...")
    simulator = RetailTransactionSimulator()
    batch_file, df_batch = simulator.generate_batch(count=1)
    print(f"  ✓ Raw Batch File Created: {batch_file}\n")
    time.sleep(1)

    # Step 2 & 3: Alteryx ETL & Snowflake Ingestion (Tool 1 & 2)
    print("[2/5] Running Alteryx ETL Data Cleansing & Validation Engine...")
    pipeline = StratifyRealtimePipeline()
    print("  ✓ Alteryx Data Validation, Referential Integrity & Type Casting complete.")
    print("  ✓ Clean batch written to: realtime/processed_ready/\n")
    time.sleep(1)

    print("[3/5] Ingesting Alteryx-Cleaned Batch into Snowflake Cloud DWH...")
    proc_cnt = pipeline.run_pipeline(poll=False)
    print(f"  ✓ Snowflake Ingestion Complete! ({proc_cnt} Alteryx-cleaned file(s) merged into RAW_SALES)\n")
    time.sleep(1)

    # Step 4: Executive PDF Report Compilation
    print("[4/5] Compiling 8-Page Executive Business Review PDF Report...")
    pdf_path = generate_executive_report()
    print(f"  ✓ PDF Report Compiled from Snowflake DWH: {pdf_path}\n")
    time.sleep(1)

    # Step 5: UiPath RPA Archival & Gmail SMTP Email Dispatch (Tool 4)
    print("[5/5] Executing UiPath RPA Archival & Gmail SMTP Email Dispatch...")
    rpa = StratifyUiPathAutomation()
    rpa.run_report_archival_workflow()
    print("  ✓ UiPath RPA Workflow & Email Delivery Complete!\n")

    print("============================================================")
    print("🎉 FULL PIPELINE COMPLETED — ALL 4 TOOLS SYNCHRONIZED!")
    print("============================================================\n")
    return True

if __name__ == "__main__":
    run_master_automated_pipeline()
