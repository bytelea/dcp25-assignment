import sqlite3
import mysql.connector

import configurations


def get_mysql_connection():
    """Open MySQL connection using config.MYSQL_CONFIG."""
    # full implementation as in final code


def get_sqlite_connection():
    """Open SQLite connection using config.SQLITE_DB_PATH."""
    # full implementation


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
    # full implementation


def run_with_connection(callback, *args, **kwargs):
    """Open connection, run callback(conn,...), then close."""
    # full implementation
 