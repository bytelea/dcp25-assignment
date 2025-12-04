import sqlite3
import mysql.connector
import configurations


def get_mysql_connection():
    """Open MySQL connection using config.MYSQL_CONFIG."""
    try:
        return mysql.connector.connect(**configurations.MYSQL_CONFIG)
    except mysql.connector.Error as err:
        print("Error connecting to MySQL:", err)
        return None


def get_sqlite_connection():
    """Open SQLite connection using config.SQLITE_DB_PATH."""
   try:
        return sqlite3.connect(configurations.SQLITE_DB_PATH)
    except sqlite3.Error as err:
        print("Error connecting to SQLite:", err)
        return None


def is_sqlite_connection(conn) -> bool:
    return isinstance(conn, sqlite3.Connection)


def prepare_sql(sql: str, conn) -> str:
    """
    Replace %s with ? when using SQLite, so queries work on both backends.
    """
    if is_sqlite_connection(conn):
        return sql.replace("%s", "?")
    return sql


def open_active_connection():
    """Open connection based on config.ACTIVE_DATABASE."""
    if configurations.ACTIVE_DATABASE == "mysql":
        return get_mysql_connection()
    if configurations.ACTIVE_DATABASE == "sqlite":
        return get_sqlite_connection()
    print(f"Unsupported database backend: {configurations.ACTIVE_DATABASE}")
    return None


def run_with_connection(callback, *args, **kwargs):
    """Open connection, run callback(conn,...), then close."""
    conn = open_active_connection()
    if not conn:
        return
    try:
        callback(conn, *args, **kwargs)
    finally:
        conn.close()