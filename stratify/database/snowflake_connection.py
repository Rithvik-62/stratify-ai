"""
STRATIFY — Decision Intelligence Platform
Snowflake Data Warehouse Connection & Query Layer (Thread-Safe & Deadlock-Free)
"""

import os
import sys
import threading
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Disable nanoarrow C-extension multithread lock deadlock on Windows
os.environ["PYTHON_SNOWFLAKE_USE_NANOARROW"] = "false"

# Load environment variables
load_dotenv()

# Thread lock to prevent concurrent GIL import deadlocks
_snowflake_lock = threading.Lock()

# Eagerly import snowflake connector under thread lock
try:
    with _snowflake_lock:
        import snowflake.connector
    SNOWFLAKE_IMPORT_OK = True
except Exception as _e:
    SNOWFLAKE_IMPORT_OK = False

class SnowflakeDatabaseManager:
    """Manages direct, thread-safe connectivity to Snowflake Data Warehouse (NOVAKART_DB.ANALYTICS)."""

    def __init__(self):
        self.account = os.getenv("SNOWFLAKE_ACCOUNT", "")
        self.user = os.getenv("SNOWFLAKE_USER", "")
        self.password = os.getenv("SNOWFLAKE_PASSWORD", "")
        self.database = os.getenv("SNOWFLAKE_DATABASE", "NOVAKART_DB")
        self.schema = os.getenv("SNOWFLAKE_SCHEMA", "ANALYTICS")
        self.warehouse = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
        self.role = os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN")

        self.conn = None
        self.is_connected = False
        self.last_sync_time = None
        self.error_message = None

        self.test_connection()

    def test_connection(self):
        """Tests Snowflake connection at application startup in a thread-safe manner."""
        with _snowflake_lock:
            self.account = os.getenv("SNOWFLAKE_ACCOUNT", "")
            self.user = os.getenv("SNOWFLAKE_USER", "")
            self.password = os.getenv("SNOWFLAKE_PASSWORD", "")
            self.database = os.getenv("SNOWFLAKE_DATABASE", "NOVAKART_DB")
            self.schema = os.getenv("SNOWFLAKE_SCHEMA", "ANALYTICS")
            self.warehouse = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
            self.role = os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN")

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

                import snowflake.connector
                self.conn = snowflake.connector.connect(**kwargs)
                self.is_connected = True
                self.last_sync_time = datetime.now()
                self.error_message = None
                return True
            except Exception as e:
                self.is_connected = False
                self.error_message = str(e)
                return False

    def query(self, sql_query):
        """Executes SQL query directly against Snowflake data warehouse using thread lock."""
        with _snowflake_lock:
            if not self.is_connected or not self.conn:
                if not self._reconnect_nolock():
                    return None

            try:
                cursor = self.conn.cursor()
                cursor.execute(sql_query)
                
                # Fetch data safely without nanoarrow deadlock
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
                # Retry once on connection drop
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
        """Helper to reconnect without taking extra lock."""
        try:
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
            self.last_sync_time = datetime.now()
            self.error_message = None
            return True
        except Exception as e:
            self.is_connected = False
            self.error_message = str(e)
            return False

    def get_status(self):
        """Returns connection status label and details."""
        if self.is_connected:
            return "● LIVE — SNOWFLAKE CONNECTED", True
        return "● OFFLINE — DATA SOURCE UNAVAILABLE", False

# Global database manager instance
db = SnowflakeDatabaseManager()
db_manager = db
