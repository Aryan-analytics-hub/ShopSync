import tkinter as tk
from tkinter import messagebox, ttk

import customtkinter as ctk
import pyodbc

from database import get_connection
from gui.widgets.table_style import setup_table_style


class ProductPage(ctk.CTkFrame):
    columns = (
        "id",
        "product",
        "description",
        "category",
        "supplier",
        "cost",
        "selling",
    )

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.search_var = tk.StringVar()
        self.summary_var = tk.StringVar(value="Loading products...")

        self.product_id_var = tk.StringVar()
        self.product_name_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.cost_price_var = tk.StringVar()
        self.selling_price_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.supplier_var = tk.StringVar()

        self.category_map = {}
        self.supplier_map = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=3)
        
        self._build_header()
        self._build_table()
        self._load_reference_data()
        self.load_products()

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
            text="Products",
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
            height=38,
            textvariable=self.search_var,
            placeholder_text="Search by product name"
        )
        self.search_entry.grid(row=0, column=0, padx=(0, 10))
        self.search_entry.bind("<Return>", self._on_search_enter)

        search_button = ctk.CTkButton(
            search_frame,
            text="Search",
            width=90,
            height=38,
            corner_radius=10,
            command=self.search_products
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
        form_card.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self._add_entry(form_card, "Product ID", self.product_id_var, 0, 0, state="readonly")
        self._add_entry(form_card, "Product Name", self.product_name_var, 0, 1)
        self._add_entry(form_card, "Cost Price", self.cost_price_var, 0, 2)
        self._add_entry(form_card, "Selling Price", self.selling_price_var, 0, 3)

        self._add_entry(form_card, "Description", self.description_var, 1, 0, columnspan=2)
        self._add_combo(form_card, "Category", self.category_var, 1, 2)
        self._add_combo(form_card, "Supplier", self.supplier_var, 1, 3)

        button_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        button_frame.grid(row=2, column=0, columnspan=4, padx=18, pady=(4, 10), sticky="ew")

        add_button = ctk.CTkButton(
            button_frame,
            text="Add Product",
            width=110,
            height=34,
            corner_radius=10,
            command=self.add_product
        )
        add_button.grid(row=0, column=0, padx=(0, 10))

        update_button = ctk.CTkButton(
            button_frame,
            text="Update Product",
            width=110,
            height=34,
            corner_radius=10,
            fg_color="#0F766E",
            hover_color="#115E59",
            command=self.update_product
        )
        update_button.grid(row=0, column=1, padx=(0, 10))

        delete_button = ctk.CTkButton(
            button_frame,
            text="Delete Product",
            width=110,
            height=34,
            corner_radius=10,
            fg_color="#B91C1C",
            hover_color="#991B1B",
            command=self.delete_product
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
            height=34,
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

        combo = ctk.CTkComboBox(
            wrapper,
            variable=variable,
            height=34,
            state="readonly",
            values=[]
        )
        combo.grid(row=1, column=0, sticky="ew")

        if label == "Category":
            self.category_combo = combo
        else:
            self.supplier_combo = combo

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
        table_card.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            table_frame,
            columns=self.columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "product": "Product",
            "description": "Description",
            "category": "Category",
            "supplier": "Supplier",
            "cost": "Cost Price",
            "selling": "Selling Price",
        }

        widths = {
            "id": 80,
            "product": 180,
            "description": 350,
            "category": 180,
            "supplier": 180,
            "cost": 130,
            "selling": 110,
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
        self.search_products()

    def _load_reference_data(self):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT CategoryID, CategoryName
                FROM Categories
                ORDER BY CategoryName
            """)
            categories = cursor.fetchall()

            cursor.execute("""
                SELECT SupplierID, SupplierName
                FROM Suppliers
                ORDER BY SupplierName
            """)
            suppliers = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

        self.category_map = {
            f"{row.CategoryID} - {row.CategoryName}": row.CategoryID
            for row in categories
        }
        self.supplier_map = {
            f"{row.SupplierID} - {row.SupplierName}": row.SupplierID
            for row in suppliers
        }

        category_values = list(self.category_map.keys())
        supplier_values = list(self.supplier_map.keys())

        self.category_combo.configure(values=category_values)
        self.supplier_combo.configure(values=supplier_values)

        if category_values:
            self.category_var.set(category_values[0])
        if supplier_values:
            self.supplier_var.set(supplier_values[0])

    def _fetch_products(self, product_name=None):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            query = """
                SELECT
                    P.ProductID,
                    P.ProductName,
                    P.Description,
                    C.CategoryName,
                    S.SupplierName,
                    P.CostPrice,
                    P.SellingPrice
                FROM Products AS P
                INNER JOIN Categories AS C
                    ON P.CategoryID = C.CategoryID
                INNER JOIN Suppliers AS S
                    ON P.SupplierID = S.SupplierID
            """

            params = None

            if product_name:
                query += " WHERE P.ProductName LIKE ?"
                params = (f"%{product_name}%",)

            query += " ORDER BY P.ProductID"

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

        for product in rows:
            self.tree.insert(
                "",
                "end",
                values=(
                    product.ProductID,
                    product.ProductName,
                    product.Description or "",
                    product.CategoryName,
                    product.SupplierName,
                    f"Rs {product.CostPrice}",
                    f"Rs {product.SellingPrice}",
                )
            )

    def _parse_form_values(self):
        product_name = self.product_name_var.get().strip()
        description = self.description_var.get().strip()
        category_label = self.category_var.get().strip()
        supplier_label = self.supplier_var.get().strip()

        if not product_name:
            raise ValueError("Product name cannot be empty.")

        try:
            cost_price = float(self.cost_price_var.get().strip())
            selling_price = float(self.selling_price_var.get().strip())
        except ValueError as error:
            raise ValueError("Cost price and selling price must be numeric.") from error

        if cost_price < 0:
            raise ValueError("Cost price cannot be negative.")

        if selling_price < 0:
            raise ValueError("Selling price cannot be negative.")

        if selling_price < cost_price:
            raise ValueError("Selling price cannot be less than cost price.")

        category_id = self.category_map.get(category_label)
        supplier_id = self.supplier_map.get(supplier_label)

        if category_id is None:
            raise ValueError("Select a valid category.")

        if supplier_id is None:
            raise ValueError("Select a valid supplier.")

        return (
            product_name,
            description,
            cost_price,
            selling_price,
            supplier_id,
            category_id,
        )

    def on_row_select(self, _event):
        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(selected[0], "values")

        self.product_id_var.set(values[0])
        self.product_name_var.set(values[1])
        self.description_var.set(values[2])
        self.cost_price_var.set(str(values[5]).replace("Rs ", ""))
        self.selling_price_var.set(str(values[6]).replace("Rs ", ""))

        category_name = values[3]
        supplier_name = values[4]

        for label in self.category_map:
            if label.endswith(f"- {category_name}"):
                self.category_var.set(label)
                break

        for label in self.supplier_map:
            if label.endswith(f"- {supplier_name}"):
                self.supplier_var.set(label)
                break

    def clear_form(self):
        self.product_id_var.set("")
        self.product_name_var.set("")
        self.description_var.set("")
        self.cost_price_var.set("")
        self.selling_price_var.set("")
        self.search_var.set("")

        if self.category_map:
            self.category_var.set(list(self.category_map.keys())[0])
        else:
            self.category_var.set("")

        if self.supplier_map:
            self.supplier_var.set(list(self.supplier_map.keys())[0])
        else:
            self.supplier_var.set("")

        for selected in self.tree.selection():
            self.tree.selection_remove(selected)

        self.summary_var.set("Form cleared")

    def refresh_page(self):
        self._load_reference_data()
        self.load_products()
        self.clear_form()

    def load_products(self):
        try:
            rows = self._fetch_products()
            self._populate_table(rows)
            self.summary_var.set(f"{len(rows)} products loaded from the database")
        except Exception as error:
            self._populate_table([])
            self.summary_var.set(f"Failed to load products: {error}")

    def search_products(self):
        search_text = self.search_var.get().strip()

        try:
            rows = self._fetch_products(search_text if search_text else None)
            self._populate_table(rows)

            if search_text:
                self.summary_var.set(
                    f"{len(rows)} matching products for '{search_text}'"
                )
            else:
                self.summary_var.set(f"{len(rows)} products loaded from the database")
        except Exception as error:
            self._populate_table([])
            self.summary_var.set(f"Search failed: {error}")

    def add_product(self):
        conn = None
        cursor = None

        try:
            values = self._parse_form_values()

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO Products
                (
                    ProductName,
                    Description,
                    CostPrice,
                    SellingPrice,
                    SupplierID,
                    CategoryID
                )
                OUTPUT INSERTED.ProductID
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                values
            )

            product_id = cursor.fetchone()[0]

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
                    0,
                    10,
                )
            )

            conn.commit()

            self.load_products()
            self.clear_form()
            self.summary_var.set(f"Product {product_id} added successfully")
            messagebox.showinfo("Success", "Product added successfully.")
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))
        except pyodbc.IntegrityError as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Could not add product.\n\n{error}")
        except Exception as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Unexpected Error", str(error))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_product(self):
        conn = None
        cursor = None

        try:
            product_id = self.product_id_var.get().strip()

            if not product_id:
                raise ValueError("Select a product from the table to update.")

            values = self._parse_form_values()

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE Products
                SET
                    ProductName = ?,
                    Description = ?,
                    CostPrice = ?,
                    SellingPrice = ?,
                    SupplierID = ?,
                    CategoryID = ?
                WHERE ProductID = ?
                """,
                values + (int(product_id),)
            )

            if cursor.rowcount == 0:
                raise ValueError("Product not found.")

            conn.commit()

            self.load_products()
            self.summary_var.set(f"Product {product_id} updated successfully")
            messagebox.showinfo("Success", "Product updated successfully.")
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))
        except pyodbc.IntegrityError as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Could not update product.\n\n{error}")
        except Exception as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Unexpected Error", str(error))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_product(self):
        conn = None
        cursor = None

        try:
            product_id = self.product_id_var.get().strip()

            if not product_id:
                raise ValueError("Select a product from the table to delete.")

            confirmed = messagebox.askyesno(
                "Confirm Delete",
                f"Delete product ID {product_id}?"
            )

            if not confirmed:
                return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM Products
                WHERE ProductID = ?
                """,
                (int(product_id),)
            )

            if cursor.rowcount == 0:
                raise ValueError("Product not found.")

            conn.commit()

            self.load_products()
            self.clear_form()
            self.summary_var.set(f"Product {product_id} deleted successfully")
            messagebox.showinfo("Success", "Product deleted successfully.")
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))
        except pyodbc.IntegrityError as error:
            if conn:
                conn.rollback()
            messagebox.showerror(
                "Database Error",
                "Could not delete product. It may still be referenced by inventory or order items.\n\n"
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
