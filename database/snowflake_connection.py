"""
STRATIFY — Decision Intelligence Platform
Snowflake Data Warehouse Connection & Query Layer (Thread-Safe, SiS & Local Compatible)
"""

import os
import sys
import threading
import pandas as pd
from datetime import datetime

# Disable nanoarrow C-extension multithread lock deadlock on Windows
os.environ["PYTHON_SNOWFLAKE_USE_NANOARROW"] = "false"

# Safely import load_dotenv if available (local development)
try:
    from dotenv import load_dotenv
    ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if os.path.exists(ENV_PATH):
        load_dotenv(dotenv_path=ENV_PATH, override=True)
    else:
        load_dotenv()
except ImportError:
    pass

# Thread lock to prevent concurrent GIL import deadlocks
_snowflake_lock = threading.Lock()

def get_config(key, default=""):
    """Fetches config value from os.getenv or st.secrets (Streamlit Cloud compatible, supporting both flat & nested TOML)."""
    val = os.getenv(key)
    if val:
        return str(val).strip()
    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            if key in st.secrets:
                return str(st.secrets[key]).strip()
            if key.upper() in st.secrets:
                return str(st.secrets[key.upper()]).strip()
            if key.lower() in st.secrets:
                return str(st.secrets[key.lower()]).strip()
            if "secrets" in st.secrets and isinstance(st.secrets["secrets"], dict):
                if key in st.secrets["secrets"]:
                    return str(st.secrets["secrets"][key]).strip()
            if "SNOWFLAKE" in st.secrets and isinstance(st.secrets["SNOWFLAKE"], dict):
                if key in st.secrets["SNOWFLAKE"]:
                    return str(st.secrets["SNOWFLAKE"][key]).strip()
    except Exception:
        pass
    return default

class SnowflakeDatabaseManager:
    """Manages direct connectivity to Snowflake Data Warehouse (SiS, Cloud & Local compatible)."""

    def __init__(self):
        self.account = get_config("SNOWFLAKE_ACCOUNT", "")
        self.user = get_config("SNOWFLAKE_USER", "")
        self.password = get_config("SNOWFLAKE_PASSWORD", "")
        self.database = get_config("SNOWFLAKE_DATABASE", "NOVAKART_DB")
        self.schema = get_config("SNOWFLAKE_SCHEMA", "ANALYTICS")
        self.warehouse = get_config("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
        self.role = get_config("SNOWFLAKE_ROLE", "ACCOUNTADMIN")

        self.conn = None
        self.snowpark_session = None
        self.is_connected = False
        self.is_sis_native = False
        self.last_sync_time = None
        self.error_message = None

        self.test_connection()

    def test_connection(self):
        """Tests Snowflake connection (Native SiS Session, st.secrets, or Local Connector)."""
        with _snowflake_lock:
            # 1. Try Native Streamlit in Snowflake (SiS) Session first
            try:
                from snowflake.snowpark.context import get_active_session
                self.snowpark_session = get_active_session()
                if self.snowpark_session:
                    self.is_connected = True
                    self.is_sis_native = True
                    self.last_sync_time = datetime.now()
                    self.error_message = None
                    return True
            except Exception:
                self.snowpark_session = None

            # 2. Connector via Environment Variables or st.secrets
            self.account = get_config("SNOWFLAKE_ACCOUNT", "")
            self.user = get_config("SNOWFLAKE_USER", "")
            self.password = get_config("SNOWFLAKE_PASSWORD", "")
            self.database = get_config("SNOWFLAKE_DATABASE", "NOVAKART_DB")
            self.schema = get_config("SNOWFLAKE_SCHEMA", "ANALYTICS")
            self.warehouse = get_config("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
            self.role = get_config("SNOWFLAKE_ROLE", "ACCOUNTADMIN")

            if not (self.account and self.user and self.password):
                self.is_connected = False
                self.error_message = "Snowflake credentials not configured in environment or .env file."
                return False

            try:
                if self.conn:
                    try:
                        self.conn.close()
                    except Exception:
                        pass
                    self.conn = None

                import snowflake.connector
                kwargs = {
                    "user": self.user,
                    "password": self.password,
                    "account": self.account,
                    "database": self.database,
                    "schema": self.schema,
                    "login_timeout": 8
                }
                if self.warehouse:
                    kwargs["warehouse"] = self.warehouse
                if self.role:
                    kwargs["role"] = self.role

                self.conn = snowflake.connector.connect(**kwargs)
                self.is_connected = True
                self.is_sis_native = False
                self.last_sync_time = datetime.now()
                self.error_message = None
                return True
            except Exception as e:
                self.is_connected = False
                self.error_message = str(e)
                return False

    def query(self, sql_query):
        """Executes SQL query against Snowflake (using Native SiS session or connector)."""
        with _snowflake_lock:
            # Native SiS Query Execution
            if self.is_sis_native and self.snowpark_session:
                try:
                    df = self.snowpark_session.sql(sql_query).to_pandas()
                    self.last_sync_time = datetime.now()
                    return df
                except Exception as e:
                    self.error_message = f"SiS Query Error: {e}"
                    return None

            # Local Connector Execution
            if not self.is_connected or not self.conn:
                if not self._reconnect_nolock():
                    return None

            try:
                cursor = self.conn.cursor()
                cursor.execute(sql_query)
                try:
                    df = cursor.fetch_pandas_all()
                except Exception:
                    rows = cursor.fetchall()
                    cols = [desc[0] for desc in cursor.description]
                    df = pd.DataFrame(rows, columns=cols)
                cursor.close()
                self.last_sync_time = datetime.now()
                return df
            except Exception as e:
                try:
                    if self._reconnect_nolock():
                        cursor = self.conn.cursor()
                        cursor.execute(sql_query)
                        rows = cursor.fetchall()
                        cols = [desc[0] for desc in cursor.description]
                        cursor.close()
                        df = pd.DataFrame(rows, columns=cols)
                        self.last_sync_time = datetime.now()
                        return df
                except Exception:
                    pass

                self.error_message = f"Query Execution Error: {e}"
                return None

    def _reconnect_nolock(self):
        """Helper to reconnect without extra lock."""
        try:
            from snowflake.snowpark.context import get_active_session
            self.snowpark_session = get_active_session()
            if self.snowpark_session:
                self.is_connected = True
                self.is_sis_native = True
                return True
        except Exception:
            pass

        try:
            self.account = get_config("SNOWFLAKE_ACCOUNT", "")
            self.user = get_config("SNOWFLAKE_USER", "")
            self.password = get_config("SNOWFLAKE_PASSWORD", "")
            self.database = get_config("SNOWFLAKE_DATABASE", "NOVAKART_DB")
            self.schema = get_config("SNOWFLAKE_SCHEMA", "ANALYTICS")
            self.warehouse = get_config("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
            self.role = get_config("SNOWFLAKE_ROLE", "ACCOUNTADMIN")

            if not (self.account and self.user and self.password):
                return False
            import snowflake.connector
            kwargs = {
                "user": self.user,
                "password": self.password,
                "account": self.account,
                "database": self.database,
                "schema": self.schema,
                "login_timeout": 8
            }
            if self.warehouse:
                kwargs["warehouse"] = self.warehouse
            if self.role:
                kwargs["role"] = self.role

            self.conn = snowflake.connector.connect(**kwargs)
            self.is_connected = True
            self.is_sis_native = False
            return True
        except Exception as e:
            self.is_connected = False
            self.error_message = str(e)
            return False

    def get_status(self):
        """Returns connection status label and details."""
        if self.is_connected:
            lbl = "● LIVE — NATIVE SNOWFLAKE" if self.is_sis_native else "● LIVE — SNOWFLAKE CONNECTED"
            return lbl, True
        return "● OFFLINE — DATA SOURCE UNAVAILABLE", False

# Global database manager instance
db = SnowflakeDatabaseManager()
db_manager = db
