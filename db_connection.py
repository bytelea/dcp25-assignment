import sqlite3
import mysql.connector
import configurations
from typing import Optional
from abc_parser import load_all_tunes

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
        
def create_tunes_table_sqlite(conn):
    """Create tunes table in SQLite if needed."""
    sql = """
    CREATE TABLE IF NOT EXISTS tunes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book TEXT,
        filename TEXT,
        x TEXT,
        t TEXT,
        r TEXT,
        m TEXT,
        k TEXT,
        body TEXT
    );
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()


def clear_tunes_table_sqlite(conn):
    """Delete all rows from the SQLite tunes table."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tunes;")
    conn.commit()
    cursor.close()


def insert_tunes_sqlite(conn, tunes):
    """Insert parsed tunes into the SQLite tunes table."""
    sql = """
    INSERT INTO tunes (book, filename, x, t, r, m, k, body)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """
    rows = [
        (
            t.get("book", ""),
            t.get("filename", ""),
            t.get("X", ""),
            t.get("T", ""),
            t.get("R", ""),
            t.get("M", ""),
            t.get("K", ""),
            t.get("body", "")
        )
        for t in tunes
    ]
    cursor = conn.cursor()
    cursor.executemany(sql, rows)
    conn.commit()
    cursor.close()
    
def create_tunes_table_mysql(conn):
    """Create tunes table in MySQL if needed."""
    sql = """
    CREATE TABLE IF NOT EXISTS tunes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        book VARCHAR(100),
        filename VARCHAR(200),
        x VARCHAR(50),
        t TEXT,
        r VARCHAR(100),
        m VARCHAR(50),
        k VARCHAR(50),
        body TEXT
    );
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()


def clear_tunes_table_mysql(conn):
    """Delete all rows from the MySQL tunes table."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tunes;")
    conn.commit()
    cursor.close()


def insert_tunes_mysql(conn, tunes):
    """Insert parsed tunes into the MySQL tunes table."""
    sql = """
    INSERT INTO tunes (book, filename, x, t, r, m, k, body)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    rows = [
        (
            t.get("book", ""),
            t.get("filename", ""),
            t.get("X", ""),
            t.get("T", ""),
            t.get("R", ""),
            t.get("M", ""),
            t.get("K", ""),
            t.get("body", "")
        )
        for t in tunes
    ]
    cursor = conn.cursor()
    cursor.executemany(sql, rows)
    conn.commit()
    cursor.close()
    
def rebuild_database(target: Optional[str] = None):
    """
    Rebuild SQLite or MySQL database from ABC files.
    - loads tunes via abc_parser.load_all_tunes()
    - recreates tunes table
    - clears old data
    - inserts fresh data
    """
    target_db = (target or configurations.ACTIVE_DATABASE).strip().lower()
    if target_db not in configurations.SUPPORTED_DATABASES:
        print(f"Unsupported database backend: {target_db}")
        return

    print(f"\nRebuilding {target_db.upper()} database from ABC files...\n")
    tunes = load_all_tunes()

    if target_db == "mysql":
        conn = get_mysql_connection()
        if conn is None:
            return
        create_tunes_table_mysql(conn)
        clear_tunes_table_mysql(conn)
        insert_tunes_mysql(conn, tunes)
        conn.close()
    else:
        conn = get_sqlite_connection()
        if conn is None:
            return
        create_tunes_table_sqlite(conn)
        clear_tunes_table_sqlite(conn)
        insert_tunes_sqlite(conn, tunes)
        conn.close()

    print("\nDatabase rebuild complete.\n")
    
def fetch_all(conn, sql, params=()):
    """Execute a SELECT and return all rows."""
    cursor = conn.cursor()
    cursor.execute(prepare_sql(sql, conn), params)
    rows = cursor.fetchall()
    cursor.close()
    return rows


def fetch_one(conn, sql, params=()):
    """Execute a SELECT and return a single row (or None)."""
    cursor = conn.cursor()
    cursor.execute(prepare_sql(sql, conn), params)
    row = cursor.fetchone()
    cursor.close()
    return row