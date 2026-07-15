from tkinter import ttk


def setup_table_style():

    style = ttk.Style()

    style.theme_use("default")

    style.configure(
        "Treeview",
        background="#202938",
        foreground="white",
        fieldbackground="#202938",
        rowheight=34,
        borderwidth=0,
        font=("Segoe UI", 11)
    )

    style.map(
        "Treeview",
        background=[("selected", "#2563EB")]
    )

    style.configure(
        "Treeview.Heading",
        background="#1F2937",
        foreground="white",
        font=("Segoe UI", 11, "bold"),
        relief="flat"
    )

    style.map(
        "Treeview.Heading",
        background=[("active", "#374151")]
    )