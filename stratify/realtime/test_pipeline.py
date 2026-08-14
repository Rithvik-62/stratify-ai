"""
STRATIFY — Retail Intelligence & Data Analytics Platform
Automated Pipeline End-to-End Test Suite (test_pipeline.py)
"""

import os
import sys
import glob
import pandas as pd
from datetime import datetime

# Import modules
from generator import RetailTransactionSimulator
from pipeline import StratifyRealtimePipeline
from config import INCOMING_DIR, PROCESSED_DIR, REJECTED_DIR, LOGS_DIR, PROCESSING_LOG_PATH

def run_end_to_end_pipeline_test():
    print("=" * 68)
    print(" STRATIFY — PHASE 3 AUTOMATED PIPELINE END-TO-END TEST SUITE")
    print("=" * 68)

    sim = RetailTransactionSimulator()
    pipeline = StratifyRealtimePipeline()

    # Step 1: Generate a new valid transaction batch
    print("\n--- STEP 1: GENERATING NEW TRANSACTION BATCH ---")
    batch_path, df_gen = sim.generate_batch(count=2, testing_mode=False)
    gen_sale_ids = df_gen["Sale_ID"].tolist()
    batch_filename = os.path.basename(batch_path)
    print(f"Generated Batch: {batch_filename}")
    print(f"Sale IDs: {gen_sale_ids}")

    # Step 2: Detect CSV in incoming/
    print("\n--- STEP 2: FILE DETECTION ---")
    detected = pipeline.detect_incoming_files()
    print(f"Detected Incoming Files: {[os.path.basename(f) for f in detected]}")
    assert batch_path in detected or os.path.abspath(batch_path) in [os.path.abspath(f) for f in detected], "Generated batch not detected!"

    # Step 3: Process transaction through pipeline
    print("\n--- STEP 3: PIPELINE PROCESSING & INGESTION ---")
    res = pipeline.process_file(batch_path)
    assert res is True, "Pipeline process_file failed!"

    # Step 4: Verify RAW_SALES update
    print("\n--- STEP 4: VERIFY RAW_SALES INGESTION ---")
    df_raw = pd.read_csv(pipeline.raw_sales_path)
    raw_sale_ids = df_raw["Sale_ID"].tolist()
    for sid in gen_sale_ids:
        assert sid in raw_sale_ids, f"Sale_ID {sid} not found in RAW_SALES!"
    print(f"Verified: All generated Sale_IDs {gen_sale_ids} successfully ingested into RAW_SALES.")

    # Step 5: Verify Duplicate Protection (MERGE logic)
    print("\n--- STEP 5: VERIFY DUPLICATE PROTECTION ---")
    raw_count_before = len(df_raw)
    # Attempt to process the same records again
    dupe_tx = sim.generate_transaction(gen_sale_ids[0], testing_mode=False)
    print(f"Attempting to re-ingest duplicate Sale_ID: {dupe_tx['Sale_ID']}")
    is_valid, reason = pipeline.validate_row(dupe_tx, set(raw_sale_ids))
    assert is_valid is False and "Duplicate" in reason, "Duplicate Sale_ID protection failed!"
    print(f"Verified: Duplicate Sale_ID correctly rejected with reason: '{reason}'.")

    # Step 6: Verify Processing Log Entry
    print("\n--- STEP 6: VERIFY LOG ENTRY IN processing_log.csv ---")
    df_log = pd.read_csv(PROCESSING_LOG_PATH)
    assert not df_log.empty, "Processing log is empty!"
    latest_log = df_log.iloc[-1].to_dict()
    print("Latest Processing Log Entry:\n", latest_log)
    assert latest_log["FILE_NAME"] == batch_filename, "Log filename mismatch!"
    assert latest_log["STATUS"] == "SUCCESS", "Log status mismatch!"

    print("\n" + "=" * 68)
    print(" ALL PHASE 3 AUTOMATED PIPELINE TESTS PASSED SUCCESSFULLY! ")
    print("=" * 68 + "\n")

if __name__ == "__main__":
    run_end_to_end_pipeline_test()
