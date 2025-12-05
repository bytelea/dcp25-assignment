import contextlib
import io
import tkinter as tk
from tkinter import messagebox, simpledialog5

import configurations
import db_connection
import db_query
import data_analysis


def start_gui():
    """Start Tkinter GUI with basic layout and output box."""
    root = tk.Tk()
    root.title("ABC Tunes Browser")

    status_text = tk.StringVar(value=f"Active database: {configurations.ACTIVE_DATABASE.upper()}")
    status_label = tk.Label(root, textvariable=status_text, anchor="w")
    status_label.pack(fill="x", padx=8, pady=4)

    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    button_frame = tk.Frame(main_frame)
    button_frame.pack(side="left", fill="y", padx=8, pady=8)

    text_container = tk.Frame(main_frame)
    text_container.pack(side="right", fill="both", expand=True, padx=8, pady=8)

    output_box = tk.Text(
        text_container,
        wrap="word",
        height=20,
        font=("Consolas", 10),
        state="disabled",
        bg="#fdfdfd",
    )

    scroll = tk.Scrollbar(text_container, command=output_box.yview)
    output_box.configure(yscrollcommand=scroll.set)
    output_box.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")

    def write_output(text: str):
        """Append text to the output box."""
        output_box.configure(state="normal")
        if output_box.index("end-1c") != "1.0":
            output_box.insert(tk.END, "\n")
        output_box.insert(tk.END, text.strip() + "\n")
        output_box.configure(state="disabled")
        output_box.see(tk.END)

    def run_and_log(action, *args):
        """
        Run a function that prints to stdout and capture the output
        so it appears in the GUI instead of the terminal.
        """
        buffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(buffer):
                action(*args)
        except Exception as exc:
            messagebox.showerror("Error", str(exc), parent=root)
            return
        text = buffer.getvalue().strip() or "Done."
        write_output(text)

    def ask_text(title, prompt):
        """Ask the user for a text value (e.g. search keyword)."""
        value = simpledialog.askstring(title, prompt, parent=root)
        if value:
            return value.strip()
        return None

    def ask_number(title, prompt):
        """Ask the user for a tune id."""
        value = simpledialog.askinteger(title, prompt, parent=root, minvalue=0)
        return value

# button handlers
    def do_rebuild():
        run_and_log(db_connection.rebuild_database)

    def do_list_tunes():
        run_and_log(db_connection.run_with_connection, db_query.list_tunes)

    def do_search_title():
        keyword = ask_text("Search by title", "Enter part of the title:")
        if keyword:
            run_and_log(db_connection.run_with_connection, db_query.search_by_title, keyword)

    def do_search_key():
        key_sig = ask_text("Search by key", "Enter key (eg D, G, Em):")
        if key_sig:
            run_and_log(db_connection.run_with_connection, db_query.search_by_key, key_sig)

    def do_search_meter():
        meter = ask_text("Search by meter", "Enter meter (eg 4/4, 6/8):")
        if meter:
            run_and_log(db_connection.run_with_connection, db_query.search_by_meter, meter)

    def do_show_details():
        tune_id = ask_number("Show tune details", "Enter tune ID:")
        if tune_id is not None:
            run_and_log(db_connection.run_with_connection, db_query.show_tune_details, tune_id)

    def do_basic_stats():
        run_and_log(db_connection.run_with_connection, data_analysis.show_basic_stats_with_pandas)

    def do_pandas_analysis():
        """
        Simple text-based submenu for pandas analysis inside the GUI.
        """
        conn = db_connection.open_active_connection()
        if not conn:
            return
        df = data_analysis.load_tunes_dataframe(conn)
        conn.close()

        if df.empty:
            write_output("No tunes available. Rebuild the database first.")
            return

        menu = (
            "Choose an option:\n"
            "1. Tunes by book\n"
            "2. Tunes by rhythm/type\n"
            "3. Search tunes by title\n"
            "4. Show basic statistics"
        )
        choice = ask_text("Pandas analysis", menu)
        if not choice:
            return

        if choice == "1":
            book = ask_text("Tunes by book", "Enter book number (folder name):")
            if book:
                matches = data_analysis.get_tunes_by_book(df, book)
                run_and_log(data_analysis.print_tune_rows, matches)
        elif choice == "2":
            rhythm = ask_text("Tunes by rhythm", "Enter rhythm/type keyword (e.g. jig, reel):")
            if rhythm:
                matches = data_analysis.get_tunes_by_type(df, rhythm)
                run_and_log(data_analysis.print_tune_rows, matches)
        elif choice == "3":
            term = ask_text("Search tunes", "Enter title keyword:")
            if term:
                matches = data_analysis.search_tunes(df, term)
                run_and_log(data_analysis.print_tune_rows, matches)
        elif choice == "4":
            run_and_log(data_analysis.display_basic_stats, df)
        else:
            messagebox.showinfo("Pandas analysis", "Please choose 1–4 only.")

    def do_switch_backend():
        new_backend = ask_text("Switch backend", "Enter backend (sqlite/mysql):")
        if new_backend:
            run_and_log(configurations.set_active_database, new_backend)
            status_text.set(f"Active database: {configurations.ACTIVE_DATABASE.upper()}")

    def do_exit():
        root.destroy()

    buttons = [
        ("1. (Re)build database",       do_rebuild),
        ("2. List first 20 tunes",      do_list_tunes),
        ("3. Search by title",          do_search_title),
        ("4. Search by key",            do_search_key),
        ("5. Search by meter",          do_search_meter),
        ("6. Show tune details",        do_show_details),
        ("7. Show basic statistics",    do_basic_stats),
        ("8. Pandas analysis submenu",  do_pandas_analysis),
        ("9. Switch database backend",  do_switch_backend),
        ("0. Exit",                     do_exit),
    ]

    for text, handler in buttons:
        tk.Button(
            button_frame,
            text=text,
            anchor="w",
            width=28,
            command=handler,
            padx=6,
            pady=4,
        ).pack(fill="x", pady=3)

    write_output("Welcome to ABC Tunes! Use the buttons on the left to run an action.")
    root.mainloop()