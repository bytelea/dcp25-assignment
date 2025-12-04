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
    
def get_tunes_by_book(df: pd.DataFrame, book_number: str) -> pd.DataFrame:
    """Return all tunes for a given book identifier."""
    book_str = book_number.strip()
    return df[df["book"].astype(str) == book_str]


def get_tunes_by_type(df: pd.DataFrame, tune_type: str) -> pd.DataFrame:
    """Return tunes that match the provided rhythm/type (column R)."""
    pattern = tune_type.strip()
    if not pattern:
        return df.iloc[0:0]
    return df[df["R"].fillna("").str.contains(pattern, case=False, na=False)]


def search_tunes(df: pd.DataFrame, search_term: str) -> pd.DataFrame:
    """Search tunes by title in a case-insensitive fashion."""
    term = search_term.strip()
    if not term:
        return df.iloc[0:0]
    return df[df["T"].fillna("").str.contains(term, case=False, na=False)]


def print_tune_rows(df: pd.DataFrame, max_rows: int = 10):
    """Pretty-print up to max_rows tunes from the DataFrame."""
    if df.empty:
        print("No matching tunes found.")
        return
    preview = df[["book", "filename", "X", "T", "R", "K", "M"]].head(max_rows)
    print(preview.to_string(index=False))
    if len(df) > max_rows:
        print(f"... and {len(df) - max_rows} more")