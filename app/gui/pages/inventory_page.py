import tkinter as tk
from tkinter import messagebox, ttk

import customtkinter as ctk
import pyodbc

from database import get_connection
from gui.widgets.table_style import setup_table_style


class InventoryPage(ctk.CTkFrame):
    columns = (
        "inventory_id",
        "product_id",
        "product_name",
        "quantity",
        "reorder_level",
        "last_updated",
    )

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.search_var = tk.StringVar()
        self.summary_var = tk.StringVar(value="Loading inventory...")

        self.inventory_id_var = tk.StringVar()
        self.product_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        self.reorder_level_var = tk.StringVar()
        self.last_updated_var = tk.StringVar()

        self.product_map = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_table()
        self._load_products()
        self.load_inventory()

    def _build_header(self):
        header = ctk.CTkFrame(
            self,
            fg_color="#1F2937",
            corner_radius=20,
            border_width=1,
            border_color="#334155"
        )
        header.grid(row=0, column=0, padx=24, pady=(24, 18), sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(
            header,
            text="Inventory",
            font=("Segoe UI", 30, "bold"),
            text_color="white"
        )
        title.grid(row=0, column=0, padx=24, pady=(22, 6), sticky="w")

        subtitle = ctk.CTkLabel(
            header,
            textvariable=self.summary_var,
            font=("Segoe UI", 14),
            text_color="#CBD5E1"
        )
        subtitle.grid(row=1, column=0, padx=24, pady=(0, 20), sticky="w")

        search_frame = ctk.CTkFrame(header, fg_color="transparent")
        search_frame.grid(row=0, column=1, rowspan=2, padx=24, pady=20, sticky="e")

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=250,
            height=38,
            textvariable=self.search_var,
            placeholder_text="Search by product ID"
        )
        self.search_entry.grid(row=0, column=0, padx=(0, 10))
        self.search_entry.bind("<Return>", self._on_search_enter)

        search_button = ctk.CTkButton(
            search_frame,
            text="Search",
            width=90,
            height=38,
            corner_radius=10,
            command=self.search_inventory
        )
        search_button.grid(row=0, column=1, padx=(0, 10))

        refresh_button = ctk.CTkButton(
            search_frame,
            text="Refresh",
            width=90,
            height=38,
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
        form_card.grid_columnconfigure((0, 1, 2), weight=1)

        self._add_entry(form_card, "Inventory ID", self.inventory_id_var, 0, 0, state="readonly")
        self._add_combo(form_card, "Product", self.product_var, 0, 1)
        self._add_entry(form_card, "Last Updated", self.last_updated_var, 0, 2, state="readonly")

        self._add_entry(form_card, "Quantity", self.quantity_var, 1, 0)
        self._add_entry(form_card, "Reorder Level", self.reorder_level_var, 1, 1)

        button_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        button_frame.grid(row=2, column=0, columnspan=3, padx=18, pady=(6, 18), sticky="ew")

        add_button = ctk.CTkButton(
            button_frame,
            text="Add Inventory",
            width=120,
            height=40,
            corner_radius=10,
            command=self.add_inventory
        )
        add_button.grid(row=0, column=0, padx=(0, 10))

        update_button = ctk.CTkButton(
            button_frame,
            text="Update Inventory",
            width=130,
            height=40,
            corner_radius=10,
            fg_color="#0F766E",
            hover_color="#115E59",
            command=self.update_inventory
        )
        update_button.grid(row=0, column=1, padx=(0, 10))

        delete_button = ctk.CTkButton(
            button_frame,
            text="Delete Inventory",
            width=130,
            height=40,
            corner_radius=10,
            fg_color="#B91C1C",
            hover_color="#991B1B",
            command=self.delete_inventory
        )
        delete_button.grid(row=0, column=2, padx=(0, 10))

        clear_button = ctk.CTkButton(
            button_frame,
            text="Clear Form",
            width=110,
            height=40,
            corner_radius=10,
            fg_color="#334155",
            hover_color="#475569",
            command=self.clear_form
        )
        clear_button.grid(row=0, column=3)

    def _add_entry(self, master, label, variable, row, column, columnspan=1, state="normal"):
        wrapper = ctk.CTkFrame(master, fg_color="transparent")
        wrapper.grid(row=row, column=column, columnspan=columnspan, padx=18, pady=10, sticky="ew")
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
            height=38,
            state=state
        )
        entry.grid(row=1, column=0, sticky="ew")

        return entry

    def _add_combo(self, master, label, variable, row, column):
        wrapper = ctk.CTkFrame(master, fg_color="transparent")
        wrapper.grid(row=row, column=column, padx=18, pady=10, sticky="ew")
        wrapper.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            wrapper,
            text=label,
            font=("Segoe UI", 13, "bold"),
            text_color="#E2E8F0"
        ).grid(row=0, column=0, pady=(0, 6), sticky="w")

        self.product_combo = ctk.CTkComboBox(
            wrapper,
            variable=variable,
            height=38,
            state="readonly",
            values=[]
        )
        self.product_combo.grid(row=1, column=0, sticky="ew")

    def _build_table(self):
        table_card = ctk.CTkFrame(
            self,
            fg_color="#1F2937",
            corner_radius=20,
            border_width=1,
            border_color="#334155"
        )
        table_card.grid(row=1, column=0, padx=24, pady=(0, 24), sticky="nsew")
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(0, weight=1)

        setup_table_style()

        table_frame = tk.Frame(table_card, bg="#1F2937", highlightthickness=0)
        table_frame.grid(row=0, column=0, padx=18, pady=18, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            table_frame,
            columns=self.columns,
            show="headings"
        )

        headings = {
            "inventory_id": "Inventory ID",
            "product_id": "Product ID",
            "product_name": "Product",
            "quantity": "Quantity",
            "reorder_level": "Reorder Level",
            "last_updated": "Last Updated",
        }

        widths = {
            "inventory_id": 110,
            "product_id": 100,
            "product_name": 220,
            "quantity": 110,
            "reorder_level": 130,
            "last_updated": 180,
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
        self.search_inventory()

    def _load_products(self):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT ProductID, ProductName
                FROM Products
                ORDER BY ProductName
                """
            )
            products = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

        self.product_map = {
            f"{row.ProductID} - {row.ProductName}": row.ProductID
            for row in products
        }

        product_values = list(self.product_map.keys())
        self.product_combo.configure(values=product_values)

        if product_values:
            self.product_var.set(product_values[0])
        else:
            self.product_var.set("")

    def _fetch_inventory(self, product_id=None):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            query = """
                SELECT
                    I.InventoryID,
                    I.ProductID,
                    P.ProductName,
                    I.Quantity,
                    I.ReorderLevel,
                    I.LastUpdated
                FROM Inventory AS I
                INNER JOIN Products AS P
                    ON I.ProductID = P.ProductID
            """

            params = None

            if product_id is not None:
                query += " WHERE I.ProductID = ?"
                params = (product_id,)

            query += " ORDER BY I.InventoryID"

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

        for inventory in rows:
            self.tree.insert(
                "",
                "end",
                values=(
                    inventory.InventoryID,
                    inventory.ProductID,
                    inventory.ProductName,
                    inventory.Quantity,
                    inventory.ReorderLevel,
                    str(inventory.LastUpdated or ""),
                )
            )

    def _parse_form_values(self):
        product_label = self.product_var.get().strip()

        try:
            quantity = int(self.quantity_var.get().strip())
            reorder_level = int(self.reorder_level_var.get().strip())
        except ValueError as error:
            raise ValueError("Quantity and reorder level must be numeric.") from error

        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        if reorder_level < 0:
            raise ValueError("Reorder level cannot be negative.")

        product_id = self.product_map.get(product_label)

        if product_id is None:
            raise ValueError("Select a valid product.")

        return product_id, quantity, reorder_level

    def on_row_select(self, _event):
        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(selected[0], "values")

        self.inventory_id_var.set(values[0])
        self.quantity_var.set(values[3])
        self.reorder_level_var.set(values[4])
        self.last_updated_var.set(values[5])

        product_id = values[1]
        product_name = values[2]

        for label in self.product_map:
            if label == f"{product_id} - {product_name}":
                self.product_var.set(label)
                break

    def clear_form(self):
        self.inventory_id_var.set("")
        self.quantity_var.set("")
        self.reorder_level_var.set("")
        self.last_updated_var.set("")
        self.search_var.set("")

        if self.product_map:
            self.product_var.set(list(self.product_map.keys())[0])
        else:
            self.product_var.set("")

        for selected in self.tree.selection():
            self.tree.selection_remove(selected)

        self.summary_var.set("Form cleared")

    def refresh_page(self):
        self._load_products()
        self.load_inventory()
        self.clear_form()

    def load_inventory(self):
        try:
            rows = self._fetch_inventory()
            self._populate_table(rows)
            self.summary_var.set(f"{len(rows)} inventory records loaded from the database")
        except Exception as error:
            self._populate_table([])
            self.summary_var.set(f"Failed to load inventory: {error}")

    def search_inventory(self):
        search_text = self.search_var.get().strip()

        try:
            if search_text:
                product_id = int(search_text)
                rows = self._fetch_inventory(product_id)
                self.summary_var.set(
                    f"{len(rows)} inventory records for product ID {product_id}"
                )
            else:
                rows = self._fetch_inventory()
                self.summary_var.set(f"{len(rows)} inventory records loaded from the database")

            self._populate_table(rows)
        except ValueError:
            self._populate_table([])
            self.summary_var.set("Search failed: Product ID must be numeric.")
        except Exception as error:
            self._populate_table([])
            self.summary_var.set(f"Search failed: {error}")

    def add_inventory(self):
        conn = None
        cursor = None

        try:
            product_id, quantity, reorder_level = self._parse_form_values()

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT InventoryID
                FROM Inventory
                WHERE ProductID = ?
                """,
                (product_id,)
            )

            if cursor.fetchone() is not None:
                raise ValueError(
                    "Inventory already exists for this product. Inventory is automatically created when a product is added."
                )

            cursor.execute(
                """
                INSERT INTO Inventory
                (
                    ProductID,
                    Quantity,
                    ReorderLevel
                )
                VALUES (?, ?, ?)
                """,
                (
                    product_id,
                    quantity,
                    reorder_level,
                )
            )

            conn.commit()

            self.load_inventory()
            self.clear_form()
            self.summary_var.set(f"Inventory added for product {product_id}")
            messagebox.showinfo("Success", "Inventory added successfully.")
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))
        except pyodbc.IntegrityError as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Could not add inventory.\n\n{error}")
        except Exception as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Unexpected Error", str(error))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_inventory(self):
        conn = None
        cursor = None

        try:
            product_id, quantity, reorder_level = self._parse_form_values()

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE Inventory
                SET
                    Quantity = ?,
                    ReorderLevel = ?
                WHERE ProductID = ?
                """,
                (
                    quantity,
                    reorder_level,
                    product_id,
                )
            )

            if cursor.rowcount == 0:
                raise ValueError("Inventory record not found.")

            conn.commit()

            self.load_inventory()
            self.summary_var.set(f"Inventory updated for product {product_id}")
            messagebox.showinfo("Success", "Inventory updated successfully.")
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))
        except pyodbc.IntegrityError as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Could not update inventory.\n\n{error}")
        except Exception as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Unexpected Error", str(error))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_inventory(self):
        conn = None
        cursor = None

        try:
            product_label = self.product_var.get().strip()
            product_id = self.product_map.get(product_label)

            if product_id is None:
                raise ValueError("Select a valid product to delete inventory.")

            confirmed = messagebox.askyesno(
                "Confirm Delete",
                f"Delete inventory for product ID {product_id}?"
            )

            if not confirmed:
                return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM Inventory
                WHERE ProductID = ?
                """,
                (product_id,)
            )

            if cursor.rowcount == 0:
                raise ValueError("Inventory record not found.")

            conn.commit()

            self.load_inventory()
            self.clear_form()
            self.summary_var.set(f"Inventory deleted for product {product_id}")
            messagebox.showinfo("Success", "Inventory deleted successfully.")
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))
        except pyodbc.IntegrityError as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Could not delete inventory.\n\n{error}")
        except Exception as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Unexpected Error", str(error))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
