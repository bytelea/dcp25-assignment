import pandas as pd


def load_tunes_dataframe(conn) -> pd.DataFrame:
    """Load the entire tunes table into a pandas DataFrame."""
    return pd.read_sql("SELECT * FROM tunes;", conn)


def display_basic_stats(df: pd.DataFrame):
    """Print simple descriptive stats for the tunes dataset."""
    print("\n========== DATA ANALYSIS (pandas) ==========")
    print(f"Total number of tunes: {len(df)}\n")

    print("Tunes per book:")
    print(df["book"].value_counts())
    print()

    print("Top 10 keys by tune count:")
    print(df["k"].value_counts().head(10))
    print()

    print("Meters used:")
    print(df["m"].value_counts())
    print("============================================\n")


def show_basic_stats_with_pandas(conn):
    """Load data into pandas and show summary statistics."""
    df = load_tunes_dataframe(conn)
    if df.empty:
        print("No tunes found in the database. Rebuild it first.")
        return
    display_basic_stats(df)