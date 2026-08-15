"""
STRATIFY — Native Streamlit in Snowflake (SiS) Deployment Script (deploy_to_snowflake.py)

Deploys the STRATIFY Decision Intelligence Platform directly into Snowflake Data Warehouse.
"""

import os
import sys
import glob
from database.snowflake_connection import db

def deploy_streamlit_to_snowflake():
    """Uploads application code to Snowflake stage and creates native Streamlit object."""
    print("============================================================")
    print("STRATIFY — NATIVE STREAMLIT IN SNOWFLAKE (SiS) DEPLOYMENT")
    print("============================================================")

    if not db.is_connected:
        print(f"Error: Unable to connect to Snowflake DWH. {db.error_message}")
        return False

    cursor = db.conn.cursor()
    try:
        # 1. Ensure Database, Schema, and Stage exist
        print("[1/4] Ensuring Stage `@NOVAKART_DB.ANALYTICS.STRATIFY_APP_STAGE` exists...")
        cursor.execute("USE DATABASE NOVAKART_DB")
        cursor.execute("USE SCHEMA ANALYTICS")
        cursor.execute("CREATE OR REPLACE STAGE NOVAKART_DB.ANALYTICS.STRATIFY_APP_STAGE")
        cursor.execute("REMOVE @NOVAKART_DB.ANALYTICS.STRATIFY_APP_STAGE")
        print("  [OK] Stage created & cleared.")

        # 2. Upload Files to Stage
        print("[2/4] Uploading application files to Snowflake Stage...")
        
        # Upload root files
        root_dir = os.path.dirname(os.path.abspath(__file__))
        app_py_path = os.path.join(root_dir, "app.py").replace("\\", "/")
        env_yml_path = os.path.join(root_dir, "environment.yml").replace("\\", "/")

        cursor.execute(f"PUT 'file://{app_py_path}' @NOVAKART_DB.ANALYTICS.STRATIFY_APP_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE")
        cursor.execute(f"PUT 'file://{env_yml_path}' @NOVAKART_DB.ANALYTICS.STRATIFY_APP_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE")
        print("  [OK] Uploaded app.py and environment.yml to root stage.")

        # Upload sub-packages (database, analytics, components, ai, reports, uipath, Output)
        subdirs = ["database", "analytics", "components", "ai", "reports", "uipath", "Output"]
        for sub in subdirs:
            sub_path = os.path.join(root_dir, sub)
            if os.path.exists(sub_path):
                files = glob.glob(os.path.join(sub_path, "*.*"))
                for f in files:
                    if f.endswith(".py") or f.endswith(".csv"):
                        clean_f = f.replace("\\", "/")
                        cursor.execute(f"PUT 'file://{clean_f}' @NOVAKART_DB.ANALYTICS.STRATIFY_APP_STAGE/{sub}/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE")
                print(f"  [OK] Uploaded {len(files)} file(s) from {sub}/ to stage.")

        # 3. Create Native Streamlit Object in Snowflake
        print("[3/4] Registering Native Streamlit in Snowflake (SiS) App Object...")
        create_sis_sql = """
        CREATE OR REPLACE STREAMLIT NOVAKART_DB.ANALYTICS.STRATIFY_DECISION_INTELLIGENCE_APP
          ROOT_LOCATION = '@NOVAKART_DB.ANALYTICS.STRATIFY_APP_STAGE'
          MAIN_FILE = 'app.py'
          QUERY_WAREHOUSE = 'COMPUTE_WH'
          COMMENT = 'STRATIFY Decision Intelligence Executive BI Platform';
        """
        cursor.execute(create_sis_sql)
        print("  [OK] Streamlit App Object `STRATIFY_DECISION_INTELLIGENCE_APP` created successfully!")

        # 4. Generate Navigation Instructions
        print("[4/4] Generating Snowsight Access Link & Instructions...")
        account_locator = os.getenv("SNOWFLAKE_ACCOUNT", "")
        if not account_locator:
            print("  ⚠️  Warning: Set SNOWFLAKE_ACCOUNT in .env for Snowsight URL generation")
            snowsight_url = "https://app.snowflake.com - Replace with your account region"
        else:
            snowsight_url = f"https://app.snowflake.com/{account_locator}/#/streamlit-apps"
        
        print("\n============================================================")
        print("DEPLOYMENT SUCCESSFUL — STREAMLIT NATIVELY RUNNING IN SNOWFLAKE")
        print("============================================================")
        print(f"Database:   NOVAKART_DB")
        print(f"Schema:     ANALYTICS")
        print(f"App Name:   STRATIFY_DECISION_INTELLIGENCE_APP")
        print(f"Snowsight:  {snowsight_url}")
        print("============================================================\n")
        return True

    except Exception as e:
        print(f"Deployment Error: {e}")
        return False
    finally:
        cursor.close()

if __name__ == "__main__":
    deploy_streamlit_to_snowflake()
