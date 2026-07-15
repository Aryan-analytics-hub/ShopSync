import tkinter as tk
from tkinter import messagebox, ttk

import customtkinter as ctk
import pyodbc

from database import get_connection
from gui.widgets.table_style import setup_table_style


class CategoryPage(ctk.CTkFrame):
    columns = (
        "id",
        "category_name",
        "description",
    )

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.search_var = tk.StringVar()
        self.summary_var = tk.StringVar(value="Loading categories...")

        self.category_id_var = tk.StringVar()
        self.category_name_var = tk.StringVar()
        self.description_var = tk.StringVar()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_table()
        self.load_categories()

    def _build_header(self):
        header = ctk.CTkFrame(
            self,
            fg_color="#1F2937",
            corner_radius=20,
            border_width=1,
            border_color="#334155"
        )
        header.grid(row=0, column=0, padx=20, pady=(15, 10), sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(
            header,
            text="Categories",
            font=("Segoe UI", 30, "bold"),
            text_color="white"
        )
        title.grid(row=0, column=0, padx=24, pady=(12, 3), sticky="w")

        subtitle = ctk.CTkLabel(
            header,
            textvariable=self.summary_var,
            font=("Segoe UI", 14),
            text_color="#CBD5E1"
        )
        subtitle.grid(row=1, column=0, padx=24, pady=(0, 10), sticky="w")

        search_frame = ctk.CTkFrame(header, fg_color="transparent")
        search_frame.grid(row=0, column=1, rowspan=2, padx=24, pady=20, sticky="e")

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=250,
            height=34,
            textvariable=self.search_var,
            placeholder_text="Search by category name"
        )
        self.search_entry.grid(row=0, column=0, padx=(0, 10))
        self.search_entry.bind("<Return>", self._on_search_enter)

        search_button = ctk.CTkButton(
            search_frame,
            text="Search",
            width=90,
            height=34,
            corner_radius=10,
            command=self.search_categories
        )
        search_button.grid(row=0, column=1, padx=(0, 10))

        refresh_button = ctk.CTkButton(
            search_frame,
            text="Refresh",
            width=90,
            height=34,
            corner_radius=10,
            fg_color="#334155",
            hover_color="#475569",
            command=self.refresh_page
        )
        refresh_button.grid(row=0, column=2)

        form_card = ctk.CTkFrame(
            header,
            fg_color="#111827",
            corner_radius=18,
            border_width=1,
            border_color="#334155"
        )
        form_card.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=20,
            pady=(0, 20),
            sticky="ew"
        )
        form_card.grid_columnconfigure((0, 1), weight=1)

        self._add_entry(form_card, "Category ID", self.category_id_var, 0, 0, state="readonly")
        self._add_entry(form_card, "Category Name", self.category_name_var, 0, 1)
        self._add_entry(form_card, "Description", self.description_var, 1, 0, columnspan=2)

        button_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        button_frame.grid(row=2, column=0, columnspan=2, padx=18, pady=(4, 10), sticky="ew")

        add_button = ctk.CTkButton(
            button_frame,
            text="Add Category",
            width=120,
            height=34,
            corner_radius=10,
            command=self.add_category
        )
        add_button.grid(row=0, column=0, padx=(0, 10))

        update_button = ctk.CTkButton(
            button_frame,
            text="Update Category",
            width=130,
            height=34,
            corner_radius=10,
            fg_color="#0F766E",
            hover_color="#115E59",
            command=self.update_category
        )
        update_button.grid(row=0, column=1, padx=(0, 10))

        delete_button = ctk.CTkButton(
            button_frame,
            text="Delete Category",
            width=130,
            height=34,
            corner_radius=10,
            fg_color="#B91C1C",
            hover_color="#991B1B",
            command=self.delete_category
        )
        delete_button.grid(row=0, column=2, padx=(0, 10))

        clear_button = ctk.CTkButton(
            button_frame,
            text="Clear Form",
            width=110,
            height=34,
            corner_radius=10,
            fg_color="#334155",
            hover_color="#475569",
            command=self.clear_form
        )
        clear_button.grid(row=0, column=3)

    def _add_entry(self, master, label, variable, row, column, columnspan=1, state="normal"):
        wrapper = ctk.CTkFrame(master, fg_color="transparent")
        wrapper.grid(row=row, column=column, columnspan=columnspan, padx=18, pady=6, sticky="ew")
        wrapper.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            wrapper,
            text=label,
            font=("Segoe UI", 13, "bold"),
            text_color="#E2E8F0"
        ).grid(row=0, column=0, pady=(0, 6), sticky="w")

        entry = ctk.CTkEntry(
            wrapper,
            textvariable=variable,
            height=34,
            state=state
        )
        entry.grid(row=1, column=0, sticky="ew")

        return entry

    def _build_table(self):
        table_card = ctk.CTkFrame(
            self,
            fg_color="#1F2937",
            corner_radius=20,
            border_width=1,
            border_color="#334155"
        )
        table_card.grid(row=1, column=0, padx=20, pady=(5, 20), sticky="nsew")
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(0, weight=1)

        setup_table_style()

        table_frame = tk.Frame(table_card, bg="#1F2937", highlightthickness=0)
        table_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            table_frame,
            columns=self.columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "category_name": "Category",
            "description": "Description",
        }

        widths = {
            "id": 70,
            "category_name": 240,
            "description": 700,
        }

        for column in self.columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(column, width=widths[column], anchor="w", stretch=True)

        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

    def _on_search_enter(self, _event):
        self.search_categories()

    def _fetch_categories(self, category_name=None):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            query = """
                SELECT
                    CategoryID,
                    CategoryName,
                    Description
                FROM Categories
            """

            params = None

            if category_name:
                query += " WHERE CategoryName LIKE ?"
                params = (f"%{category_name}%",)

            query += " ORDER BY CategoryID"

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def _populate_table(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for category in rows:
            self.tree.insert(
                "",
                "end",
                values=(
                    category.CategoryID,
                    category.CategoryName,
                    category.Description or "",
                )
            )

    def _parse_form_values(self):
        category_name = self.category_name_var.get().strip()
        description = self.description_var.get().strip()

        if not category_name:
            raise ValueError("Category name cannot be empty.")

        if not any(ch.isalpha() for ch in category_name):
            raise ValueError("Category name must contain at least one alphabet.")

        return (
            category_name,
            description,
        )

    def on_row_select(self, _event):
        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(selected[0], "values")

        self.category_id_var.set(values[0])
        self.category_name_var.set(values[1])
        self.description_var.set(values[2])

    def clear_form(self):
        self.category_id_var.set("")
        self.category_name_var.set("")
        self.description_var.set("")
        self.search_var.set("")

        for selected in self.tree.selection():
            self.tree.selection_remove(selected)

        self.summary_var.set("Form cleared")

    def refresh_page(self):
        self.load_categories()
        self.clear_form()

    def load_categories(self):
        try:
            rows = self._fetch_categories()
            self._populate_table(rows)
            self.summary_var.set(f"{len(rows)} categories loaded from the database")
        except Exception as error:
            self._populate_table([])
            self.summary_var.set(f"Failed to load categories: {error}")

    def search_categories(self):
        search_text = self.search_var.get().strip()

        try:
            rows = self._fetch_categories(search_text if search_text else None)
            self._populate_table(rows)

            if search_text:
                self.summary_var.set(
                    f"{len(rows)} matching categories for '{search_text}'"
                )
            else:
                self.summary_var.set(f"{len(rows)} categories loaded from the database")
        except Exception as error:
            self._populate_table([])
            self.summary_var.set(f"Search failed: {error}")

    def add_category(self):
        conn = None
        cursor = None

        try:
            values = self._parse_form_values()

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO Categories
                (
                    CategoryName,
                    Description
                )
                VALUES (?, ?)
                """,
                values
            )

            conn.commit()

            self.load_categories()
            self.clear_form()
            self.summary_var.set("Category added successfully")
            messagebox.showinfo("Success", "Category added successfully.")
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))
        except pyodbc.IntegrityError as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Could not add category.\n\n{error}")
        except Exception as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Unexpected Error", str(error))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_category(self):
        conn = None
        cursor = None

        try:
            category_id = self.category_id_var.get().strip()

            if not category_id:
                raise ValueError("Select a category from the table to update.")

            values = self._parse_form_values()

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE Categories
                SET
                    CategoryName = ?,
                    Description = ?
                WHERE CategoryID = ?
                """,
                values + (int(category_id),)
            )

            if cursor.rowcount == 0:
                raise ValueError("Category not found.")

            conn.commit()

            self.load_categories()
            self.summary_var.set(f"Category {category_id} updated successfully")
            messagebox.showinfo("Success", "Category updated successfully.")
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))
        except pyodbc.IntegrityError as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Could not update category.\n\n{error}")
        except Exception as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Unexpected Error", str(error))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_category(self):
        conn = None
        cursor = None

        try:
            category_id = self.category_id_var.get().strip()

            if not category_id:
                raise ValueError("Select a category from the table to delete.")

            confirmed = messagebox.askyesno(
                "Confirm Delete",
                f"Delete category ID {category_id}?"
            )

            if not confirmed:
                return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM Categories
                WHERE CategoryID = ?
                """,
                (int(category_id),)
            )

            if cursor.rowcount == 0:
                raise ValueError("Category not found.")

            conn.commit()

            self.load_categories()
            self.clear_form()
            self.summary_var.set(f"Category {category_id} deleted successfully")
            messagebox.showinfo("Success", "Category deleted successfully.")
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))
        except pyodbc.IntegrityError as error:
            if conn:
                conn.rollback()
            messagebox.showerror(
                "Database Error",
                "Could not delete category. The category may still be assigned to products.\n\n"
                f"{error}"
            )
        except Exception as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Unexpected Error", str(error))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
