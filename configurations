# Starter code for Data Centric Programming Assignment 2025

# os is a module that lets us access the file systemr
import os 
import sqlite3
import pandas as pd
import mysql.connector
# sqlite for connecting to sqlite databases
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOKS_DIR = os.path.join(BASE_DIR, "abc_books")
SQLITE_DB_PATH = os.path.join(BASE_DIR, "tunes.db")

# load .env but used later
load_dotenv(os.path.join(BASE_DIR, ".env"))

# placeholders to be extended later
SUPPORTED_DATABASES = {"sqlite", "mysql"}
ACTIVE_DATABASE = "sqlite"
MYSQL_CONFIG = {}

# database backends
SUPPORTED_DATABASES = {"sqlite", "mysql"}

# active database backend:
ACTIVE_DATABASE = (os.getenv("ABC_DB_BACKEND") or "sqlite").strip().lower()
if ACTIVE_DATABASE not in SUPPORTED_DATABASES:
    print(f"Unsupported backend '{ACTIVE_DATABASE}', falling back to SQLite.")
    ACTIVE_DATABASE = "sqlite"

# mySQL connection settings read from environment variables file
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE"),
}


def set_active_database(choice: str):
    """Change the globally active database backend."""
    global ACTIVE_DATABASE
    normalized = (choice or "").strip().lower()
    if normalized in SUPPORTED_DATABASES:
        ACTIVE_DATABASE = normalized
        print(f"Active database switched to: {ACTIVE_DATABASE.upper()}")
    else:
        supported = ", ".join(sorted(SUPPORTED_DATABASES))
        print(f"'{choice}' is not supported. Choose from: {supported}.")