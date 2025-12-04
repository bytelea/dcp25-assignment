import contextlib
import io
import tkinter as tk
from tkinter import messagebox, simpledialog

import configurations
import db_connection


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
        output_box.configure(state="normal")
        if output_box.index("end-1c") != "1.0":
            output_box.insert(tk.END, "\n")
        output_box.insert(tk.END, text.strip() + "\n")
        output_box.configure(state="disabled")
        output_box.see(tk.END)

    def run_and_log(action, *args):
        buffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(buffer):
                action(*args)
        except Exception as exc:
            messagebox.showerror("Error", str(exc), parent=root)
            return
        text = buffer.getvalue().strip() or "Done."
        write_output(text)

    def do_rebuild():
        run_and_log(db_connection.rebuild_database)

    def do_exit():
        root.destroy()

    tk.Button(button_frame, text="(Re)build database", command=do_rebuild).pack(fill="x", pady=3)
    tk.Button(button_frame, text="Exit", command=do_exit).pack(fill="x", pady=3)

    write_output("Welcome to ABC Tunes! Basic GUI loaded.")
    root.mainloop()