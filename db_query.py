from db_connection import fetch_all, fetch_one


def list_tunes(conn, limit=20):
    """Print the first 'limit' tunes."""
    rows = fetch_all(
        conn,
        "SELECT id, t, k, m, book FROM tunes ORDER BY id LIMIT %s;",
        (limit,)
    )
    print(f"\nShowing first {len(rows)} tunes:\n")
    for tune_id, title, key_sig, meter, book in rows:
        title_short = (title or "")[:40]
        print(f"{tune_id:4d} | {title_short:40} | Key: {key_sig:6} | Meter: {meter:5} | Book: {book}")


def search_by_title(conn, keyword):
    """Search tunes where the title contains keyword."""
    rows = fetch_all(
        conn,
        "SELECT id, t, k, m, book FROM tunes WHERE t LIKE %s ORDER BY t;",
        (f"%{keyword}%",)
    )
    print(f"\nFound {len(rows)} tune(s) with '{keyword}' in the title:\n")
    for tune_id, title, key_sig, meter, book in rows:
        print(f"{tune_id:4d} | {title} | Key: {key_sig} | Meter: {meter} | Book: {book}")


def search_by_key(conn, key_sig):
    """Search tunes by key signature."""
    rows = fetch_all(
        conn,
        "SELECT id, t, k, m, book FROM tunes WHERE k LIKE %s ORDER BY t;",
        (f"%{key_sig}%",)
    )
    print(f"\nFound {len(rows)} tune(s) in key '{key_sig}':\n")
    for tune_id, title, key_value, meter, book in rows:
        print(f"{tune_id:4d} | {title} | Key: {key_value} | Meter: {meter} | Book: {book}")


def search_by_meter(conn, meter):
    """Search tunes by meter."""
    rows = fetch_all(
        conn,
        "SELECT id, t, k, m, book FROM tunes WHERE m LIKE %s ORDER BY t;",
        (f"%{meter}%",)
    )
    print(f"\nFound {len(rows)} tune(s) with meter '{meter}':\n")
    for tune_id, title, key_value, meter_value, book in rows:
        print(f"{tune_id:4d} | {title} | Key: {key_value} | Meter: {meter_value} | Book: {book}")


def show_tune_details(conn, tune_id):
    """Print details for a single tune."""
    row = fetch_one(
        conn,
        "SELECT id, book, filename, x, t, r, m, k, body FROM tunes WHERE id = %s;",
        (tune_id,)
    )
    if row is None:
        print(f"\nNo tune found with id {tune_id}\n")
        return

    (id_value, book, filename, x, t, r, m, k, body) = row
    print("\n----------- TUNE DETAILS -----------")
    print(f"ID:      {id_value}")
    print(f"Book:    {book}")
    print(f"File:    {filename}")
    print(f"X:       {x}")
    print(f"Title:   {t}")
    print(f"Rhythm:  {r}")
    print(f"Meter:   {m}")
    print(f"Key:     {k}")
    print("\nBody:\n")
    print(body)
    print("------------------------------------\n")