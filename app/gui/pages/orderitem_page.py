import tkinter as tk
from tkinter import messagebox, ttk

import customtkinter as ctk
import pyodbc

from database import get_connection
from gui.widgets.table_style import setup_table_style


class OrderItemPage(ctk.CTkFrame):
    columns = (
        "order_item_id",
        "order_id",
        "customer_name",
        "product_id",
        "product_name",
        "quantity",
        "unit_price",
        "subtotal",
    )

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.search_var = tk.StringVar()
        self.summary_var = tk.StringVar(value="Loading order items...")

        self.order_item_id_var = tk.StringVar()
        self.order_var = tk.StringVar()
        self.product_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        self.unit_price_var = tk.StringVar()
        self.subtotal_var = tk.StringVar()

        self.order_map = {}
        self.product_map = {}
        self.orderitem_window = None
        self.orderitem_tree = None

        self.quantity_var.trace_add("write", self._on_quantity_change)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_header()
        self._load_reference_data()
        self.load_order_items(update_window=False)

    def _build_header(self):
        header = ctk.CTkFrame(
            self,
            fg_color="#1F2937",
            corner_radius=20,
            border_width=1,
            border_color="#334155"
        )
        header.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)

        ctk.CTkLabel(
            header,
            text="Order Items",
            font=("Segoe UI", 30, "bold"),
            text_color="white"
        ).grid(row=0, column=0, padx=24, pady=(22, 6), sticky="w")

        ctk.CTkLabel(
            header,
            textvariable=self.summary_var,
            font=("Segoe UI", 14),
            text_color="#CBD5E1"
        ).grid(row=1, column=0, padx=24, pady=(0, 18), sticky="w")

        search_frame = ctk.CTkFrame(header, fg_color="transparent")
        search_frame.grid(row=2, column=0, columnspan=2, padx=24, pady=(0, 18), sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            height=38,
            textvariable=self.search_var,
            placeholder_text="Search by order item ID"
        )
        self.search_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.search_entry.bind("<Return>", self._on_search_enter)

        ctk.CTkButton(
            search_frame,
            text="Search",
            width=90,
            height=38,
            corner_radius=10,
            command=self.search_order_items
        ).grid(row=0, column=1, padx=(0, 10))

        ctk.CTkButton(
            search_frame,
            text="Refresh",
            width=90,
            height=38,
            corner_radius=10,
            fg_color="#334155",
            hover_color="#475569",
            command=self.refresh_page
        ).grid(row=0, column=2)

        form_card = ctk.CTkFrame(
            header,
            fg_color="#111827",
            corner_radius=18,
            border_width=1,
            border_color="#334155"
        )
        form_card.grid(row=3, column=0, columnspan=2, padx=24, pady=(0, 22), sticky="ew")
        for column in range(2):
            form_card.grid_columnconfigure(column, weight=1)

        self._add_entry(form_card, "Order Item ID", self.order_item_id_var, 0, 0, state="readonly")
        self._add_entry(form_card, "Subtotal", self.subtotal_var, 0, 1, state="readonly")

        self._add_combo(form_card, "Order", self.order_var, 1, 0, "order")
        self._add_combo(form_card, "Product", self.product_var, 1, 1, "product")

        self._add_entry(form_card, "Quantity", self.quantity_var, 2, 0)
        self._add_entry(form_card, "Unit Price", self.unit_price_var, 2, 1, state="readonly")

        button_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        button_frame.grid(row=3, column=0, columnspan=2, padx=12, pady=(2, 12), sticky="ew")
        for column in range(5):
            button_frame.grid_columnconfigure(column, weight=1)

        ctk.CTkButton(
            button_frame,
            text="View Order Items",
            width=120,
            height=40,
            corner_radius=10,
            fg_color="#334155",
            hover_color="#475569",
            command=self.open_orderitem_window
        ).grid(row=0, column=0, padx=6, sticky="ew")

        ctk.CTkButton(
            button_frame,
            text="Add Order Item",
            width=120,
            height=40,
            corner_radius=10,
            command=self.add_order_item
        ).grid(row=0, column=1, padx=6, sticky="ew")

        ctk.CTkButton(
            button_frame,
            text="Update",
            width=110,
            height=40,
            corner_radius=10,
            fg_color="#0F766E",
            hover_color="#115E59",
            command=self.update_order_item
        ).grid(row=0, column=2, padx=6, sticky="ew")

        ctk.CTkButton(
            button_frame,
            text="Delete",
            width=110,
            height=40,
            corner_radius=10,
            fg_color="#B91C1C",
            hover_color="#991B1B",
            command=self.delete_order_item
        ).grid(row=0, column=3, padx=6, sticky="ew")

        ctk.CTkButton(
            button_frame,
            text="Clear",
            width=100,
            height=40,
            corner_radius=10,
            fg_color="#475569",
            hover_color="#64748B",
            command=self.clear_form
        ).grid(row=0, column=4, padx=6, sticky="ew")

    def _add_entry(self, master, label, variable, row, column, columnspan=1, state="normal"):
        wrapper = ctk.CTkFrame(master, fg_color="transparent")
        wrapper.grid(row=row, column=column, columnspan=columnspan, padx=10, pady=6, sticky="ew")
        wrapper.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            wrapper,
            text=label,
            font=("Segoe UI", 13, "bold"),
            text_color="#E2E8F0"
        ).grid(row=0, column=0, pady=(0, 4), sticky="w")

        entry = ctk.CTkEntry(
            wrapper,
            textvariable=variable,
            height=38,
            state=state
        )
        entry.grid(row=1, column=0, sticky="ew")
        return entry

    def _add_combo(self, master, label, variable, row, column, combo_type):
        wrapper = ctk.CTkFrame(master, fg_color="transparent")
        wrapper.grid(row=row, column=column, padx=10, pady=6, sticky="ew")
        wrapper.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            wrapper,
            text=label,
            font=("Segoe UI", 13, "bold"),
            text_color="#E2E8F0"
        ).grid(row=0, column=0, pady=(0, 4), sticky="w")

        combo = ctk.CTkComboBox(
            wrapper,
            variable=variable,
            height=38,
            state="readonly",
            values=[]
        )
        combo.grid(row=1, column=0, sticky="ew")

        if combo_type == "order":
            self.order_combo = combo
        else:
            self.product_combo = combo
            combo.configure(command=self._on_product_change)

    def _build_orderitem_window(self):
        if self.orderitem_window is not None and self.orderitem_window.winfo_exists():
            self.orderitem_window.focus()
            return

        self.orderitem_window = ctk.CTkToplevel(self)
        self.orderitem_window.title("Order Items")
        self.orderitem_window.geometry("1180x540")
        self.orderitem_window.minsize(1000, 440)
        self.orderitem_window.configure(fg_color="#111827")
        self.orderitem_window.grid_columnconfigure(0, weight=1)
        self.orderitem_window.grid_rowconfigure(0, weight=1)
        self.orderitem_window.protocol("WM_DELETE_WINDOW", self._close_orderitem_window)

        table_card = ctk.CTkFrame(
            self.orderitem_window,
            fg_color="#1F2937",
            corner_radius=18,
            border_width=1,
            border_color="#334155"
        )
        table_card.grid(row=0, column=0, padx=18, pady=18, sticky="nsew")
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            table_card,
            text="Order Items",
            font=("Segoe UI", 24, "bold"),
            text_color="white"
        ).grid(row=0, column=0, padx=18, pady=(16, 10), sticky="w")

        setup_table_style()

        table_frame = tk.Frame(table_card, bg="#1F2937", highlightthickness=0)
        table_frame.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        self.orderitem_tree = ttk.Treeview(table_frame, columns=self.columns, show="headings")
        self.orderitem_tree.configure(height=18)

        headings = {
            "order_item_id": "Order Item ID",
            "order_id": "Order ID",
            "customer_name": "Customer",
            "product_id": "Product ID",
            "product_name": "Product",
            "quantity": "Quantity",
            "unit_price": "Unit Price",
            "subtotal": "Subtotal",
        }

        widths = {
            "order_item_id": 110,
            "order_id": 90,
            "customer_name": 220,
            "product_id": 90,
            "product_name": 220,
            "quantity": 90,
            "unit_price": 110,
            "subtotal": 110,
        }

        for column in self.columns:
            self.orderitem_tree.heading(column, text=headings[column])
            self.orderitem_tree.column(column, width=widths[column], anchor="w", stretch=True)

        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.orderitem_tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.orderitem_tree.xview)

        self.orderitem_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        self.orderitem_tree.bind("<<TreeviewSelect>>", self.on_row_select)

        self.orderitem_tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

    def _close_orderitem_window(self):
        if self.orderitem_window is not None and self.orderitem_window.winfo_exists():
            self.orderitem_window.destroy()
        self.orderitem_window = None
        self.orderitem_tree = None

    def open_orderitem_window(self):
        self._build_orderitem_window()
        self.load_order_items(update_window=True)

    def _on_search_enter(self, _event):
        self.search_order_items()

    def _on_product_change(self, _selected_value):
        self._sync_product_price()
        self._update_subtotal_preview()

    def _on_quantity_change(self, *_args):
        self._update_subtotal_preview()

    def _load_reference_data(self):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    O.OrderID,
                    C.FirstName,
                    C.LastName
                FROM Orders AS O
                INNER JOIN Customers AS C
                    ON O.CustomerID = C.CustomerID
                ORDER BY O.OrderID
                """
            )
            orders = cursor.fetchall()

            cursor.execute(
                """
                SELECT
                    ProductID,
                    ProductName,
                    SellingPrice
                FROM Products
                ORDER BY ProductName, ProductID
                """
            )
            products = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

        self.order_map = {
            f"{row.OrderID} - {row.FirstName} {row.LastName or ''}".strip(): row.OrderID
            for row in orders
        }
        self.product_map = {
            f"{row.ProductID} - {row.ProductName}": {
                "product_id": row.ProductID,
                "unit_price": float(row.SellingPrice),
            }
            for row in products
        }

        order_values = list(self.order_map.keys())
        product_values = list(self.product_map.keys())

        self.order_combo.configure(values=order_values)
        self.product_combo.configure(values=product_values)

        self.order_var.set(order_values[0] if order_values else "")
        self.product_var.set(product_values[0] if product_values else "")
        self._sync_product_price()
        self._update_subtotal_preview()

    def _fetch_order_items(self, order_item_id=None):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            query = """
                SELECT
                    OI.OrderItemID,
                    OI.OrderID,
                    C.FirstName,
                    C.LastName,
                    OI.ProductID,
                    P.ProductName,
                    OI.Quantity,
                    OI.UnitPrice,
                    OI.SubTotal
                FROM OrderItems AS OI
                INNER JOIN Orders AS O
                    ON OI.OrderID = O.OrderID
                INNER JOIN Customers AS C
                    ON O.CustomerID = C.CustomerID
                INNER JOIN Products AS P
                    ON OI.ProductID = P.ProductID
            """

            params = None
            if order_item_id is not None:
                query += " WHERE OI.OrderItemID = ?"
                params = (order_item_id,)

            query += " ORDER BY OI.OrderItemID"

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def _populate_table(self, rows):
        if self.orderitem_tree is None or not self.orderitem_tree.winfo_exists():
            return

        for item in self.orderitem_tree.get_children():
            self.orderitem_tree.delete(item)

        for order_item in rows:
            customer_name = f"{order_item.FirstName} {order_item.LastName or ''}".strip()
            self.orderitem_tree.insert(
                "",
                "end",
                values=(
                    order_item.OrderItemID,
                    order_item.OrderID,
                    customer_name,
                    order_item.ProductID,
                    order_item.ProductName,
                    order_item.Quantity,
                    f"{float(order_item.UnitPrice):.2f}",
                    f"{float(order_item.SubTotal):.2f}",
                )
            )

    def _selected_order_id(self):
        order_id = self.order_map.get(self.order_var.get().strip())
        if order_id is None:
            raise ValueError("Select a valid order.")
        return order_id

    def _selected_product_details(self):
        product = self.product_map.get(self.product_var.get().strip())
        if product is None:
            raise ValueError("Select a valid product.")
        return product["product_id"], product["unit_price"]

    def _parse_quantity(self):
        try:
            quantity = int(self.quantity_var.get().strip())
        except ValueError as error:
            raise ValueError("Quantity must be numeric.") from error

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        return quantity

    def _sync_product_price(self):
        product = self.product_map.get(self.product_var.get().strip())
        if product is None:
            self.unit_price_var.set("")
            return

        self.unit_price_var.set(f"{product['unit_price']:.2f}")

    def _update_subtotal_preview(self):
        try:
            quantity = int(self.quantity_var.get().strip())
            unit_price = float(self.unit_price_var.get().strip())
            if quantity > 0:
                self.subtotal_var.set(f"{quantity * unit_price:.2f}")
                return
        except ValueError:
            pass

        self.subtotal_var.set("")

    def _require_stock(self, cursor, product_id, quantity_needed):
        cursor.execute(
            """
            SELECT Quantity
            FROM Inventory
            WHERE ProductID = ?
            """,
            (product_id,)
        )
        stock = cursor.fetchone()

        if stock is None:
            raise ValueError("Inventory record not found for the selected product.")

        if stock.Quantity < quantity_needed:
            raise ValueError(f"Not enough stock available. Current stock: {stock.Quantity}.")

    def _update_inventory(self, cursor, product_id, quantity_change):
        cursor.execute(
            """
            UPDATE Inventory
            SET Quantity = Quantity + ?
            WHERE ProductID = ?
            """,
            (quantity_change, product_id)
        )

        if cursor.rowcount == 0:
            raise ValueError("Inventory record not found for the selected product.")

    def _recalculate_order_total(self, cursor, order_id):
        cursor.execute(
            """
            SELECT COALESCE(SUM(SubTotal), 0)
            FROM OrderItems
            WHERE OrderID = ?
            """,
            (order_id,)
        )
        total_amount = float(cursor.fetchone()[0] or 0)

        cursor.execute(
            """
            UPDATE Orders
            SET TotalAmount = ?
            WHERE OrderID = ?
            """,
            (total_amount, order_id)
        )

    def on_row_select(self, event):
        selected = event.widget.selection()
        if not selected:
            return

        values = event.widget.item(selected[0], "values")

        self.order_item_id_var.set(values[0])
        self.quantity_var.set(values[5])
        self.unit_price_var.set(values[6])
        self.subtotal_var.set(values[7])

        order_label = f"{values[1]} - {values[2]}"
        product_label = f"{values[3]} - {values[4]}"

        if order_label in self.order_map:
            self.order_var.set(order_label)
        if product_label in self.product_map:
            self.product_var.set(product_label)

    def clear_form(self):
        self.order_item_id_var.set("")
        self.quantity_var.set("")
        self.search_var.set("")
        self.subtotal_var.set("")

        order_values = list(self.order_map.keys())
        product_values = list(self.product_map.keys())

        self.order_var.set(order_values[0] if order_values else "")
        self.product_var.set(product_values[0] if product_values else "")
        self._sync_product_price()

        if self.orderitem_tree is not None and self.orderitem_tree.winfo_exists():
            for selected in self.orderitem_tree.selection():
                self.orderitem_tree.selection_remove(selected)

        self.summary_var.set("Form cleared")

    def refresh_page(self):
        self._load_reference_data()
        self.load_order_items(update_window=True)
        self.clear_form()

    def load_order_items(self, update_window=True):
        try:
            rows = self._fetch_order_items()
            if update_window:
                self._populate_table(rows)
            self.summary_var.set(f"{len(rows)} order items loaded from the database")
        except Exception as error:
            if update_window:
                self._populate_table([])
            self.summary_var.set(f"Failed to load order items: {error}")

    def search_order_items(self):
        search_text = self.search_var.get().strip()

        try:
            if search_text:
                order_item_id = int(search_text)
                rows = self._fetch_order_items(order_item_id)
                self.summary_var.set(f"{len(rows)} matching order items for ID {order_item_id}")
            else:
                rows = self._fetch_order_items()
                self.summary_var.set(f"{len(rows)} order items loaded from the database")

            self.open_orderitem_window()
            self._populate_table(rows)
        except ValueError:
            self.summary_var.set("Search failed: Order Item ID must be numeric.")
        except Exception as error:
            self.summary_var.set(f"Search failed: {error}")

    def add_order_item(self):
        conn = None
        cursor = None

        try:
            order_id = self._selected_order_id()
            product_id, unit_price = self._selected_product_details()
            quantity = self._parse_quantity()

            conn = get_connection()
            cursor = conn.cursor()

            self._require_stock(cursor, product_id, quantity)

            cursor.execute(
                """
                INSERT INTO OrderItems
                (
                    OrderID,
                    ProductID,
                    Quantity,
                    UnitPrice
                )
                VALUES (?, ?, ?, ?)
                """,
                (order_id, product_id, quantity, unit_price)
            )

            self._update_inventory(cursor, product_id, -quantity)
            self._recalculate_order_total(cursor, order_id)

            conn.commit()

            self.load_order_items()
            self.clear_form()
            self.summary_var.set(f"Order item added to order {order_id}")
            messagebox.showinfo("Success", "Order item added successfully.")
        except ValueError as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Invalid Input", str(error))
        except pyodbc.IntegrityError as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Could not add order item.\n\n{error}")
        except Exception as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Unexpected Error", str(error))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_order_item(self):
        conn = None
        cursor = None

        try:
            order_item_id = self.order_item_id_var.get().strip()
            if not order_item_id:
                raise ValueError("Select an order item from the table to update.")

            new_order_id = self._selected_order_id()
            new_product_id, new_unit_price = self._selected_product_details()
            new_quantity = self._parse_quantity()

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    OrderID,
                    ProductID,
                    Quantity
                FROM OrderItems
                WHERE OrderItemID = ?
                """,
                (int(order_item_id),)
            )
            existing = cursor.fetchone()

            if existing is None:
                raise ValueError("Order item not found.")

            old_order_id = existing.OrderID
            old_product_id = existing.ProductID
            old_quantity = existing.Quantity

            if old_product_id == new_product_id:
                quantity_difference = new_quantity - old_quantity
                if quantity_difference > 0:
                    self._require_stock(cursor, new_product_id, quantity_difference)
                self._update_inventory(cursor, new_product_id, -quantity_difference)
            else:
                self._require_stock(cursor, new_product_id, new_quantity)
                self._update_inventory(cursor, old_product_id, old_quantity)
                self._update_inventory(cursor, new_product_id, -new_quantity)

            cursor.execute(
                """
                UPDATE OrderItems
                SET
                    OrderID = ?,
                    ProductID = ?,
                    Quantity = ?,
                    UnitPrice = ?
                WHERE OrderItemID = ?
                """,
                (
                    new_order_id,
                    new_product_id,
                    new_quantity,
                    new_unit_price,
                    int(order_item_id),
                )
            )

            if cursor.rowcount == 0:
                raise ValueError("Order item not found.")

            self._recalculate_order_total(cursor, old_order_id)
            if new_order_id != old_order_id:
                self._recalculate_order_total(cursor, new_order_id)

            conn.commit()

            self.load_order_items()
            self.summary_var.set(f"Order item {order_item_id} updated successfully")
            messagebox.showinfo("Success", "Order item updated successfully.")
        except ValueError as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Invalid Input", str(error))
        except pyodbc.IntegrityError as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Could not update order item.\n\n{error}")
        except Exception as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Unexpected Error", str(error))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_order_item(self):
        conn = None
        cursor = None

        try:
            order_item_id = self.order_item_id_var.get().strip()
            if not order_item_id:
                raise ValueError("Select an order item from the table to delete.")

            confirmed = messagebox.askyesno(
                "Confirm Delete",
                f"Delete order item ID {order_item_id}?"
            )
            if not confirmed:
                return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    OrderID,
                    ProductID,
                    Quantity
                FROM OrderItems
                WHERE OrderItemID = ?
                """,
                (int(order_item_id),)
            )
            existing = cursor.fetchone()

            if existing is None:
                raise ValueError("Order item not found.")

            cursor.execute(
                """
                DELETE FROM OrderItems
                WHERE OrderItemID = ?
                """,
                (int(order_item_id),)
            )

            if cursor.rowcount == 0:
                raise ValueError("Order item not found.")

            self._update_inventory(cursor, existing.ProductID, existing.Quantity)
            self._recalculate_order_total(cursor, existing.OrderID)

            conn.commit()

            self.load_order_items()
            self.clear_form()
            self.summary_var.set(f"Order item {order_item_id} deleted successfully")
            messagebox.showinfo("Success", "Order item deleted successfully.")
        except ValueError as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Invalid Input", str(error))
        except pyodbc.IntegrityError as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Could not delete order item.\n\n{error}")
        except Exception as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Unexpected Error", str(error))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
