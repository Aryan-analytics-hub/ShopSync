


import tkinter as tk
from tkinter import messagebox, ttk

import customtkinter as ctk
import pyodbc

from database import get_connection
from gui.widgets.table_style import setup_table_style


class OrderPage(ctk.CTkFrame):
    columns = (
        "order_id",
        "customer_id",
        "customer_name",
        "order_date",
        "total_amount",
        "order_status",
    )

    valid_statuses = [
        "Pending",
        "Confirmed",
        "Packed",
        "Shipped",
        "Delivered",
        "Cancelled",
    ]

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.search_var = tk.StringVar()
        self.summary_var = tk.StringVar(value="Loading orders...")

        self.order_id_var = tk.StringVar()
        self.customer_var = tk.StringVar()
        self.order_date_var = tk.StringVar()
        self.total_amount_var = tk.StringVar()
        self.order_status_var = tk.StringVar()

        self.customer_map = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_table()
        self._load_customers()
        self.load_orders()

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
            text="Orders",
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
            placeholder_text="Search by order ID"
        )
        self.search_entry.grid(row=0, column=0, padx=(0, 10))
        self.search_entry.bind("<Return>", self._on_search_enter)

        search_button = ctk.CTkButton(
            search_frame,
            text="Search",
            width=90,
            height=38,
            corner_radius=10,
            command=self.search_orders
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
            padx=18,
            pady=(0, 12),
            sticky="ew"
        )
        form_card.grid_columnconfigure((0, 1, 2), weight=1)

        self._add_entry(form_card, "Order ID", self.order_id_var, 0, 0, state="readonly")
        self._add_combo(form_card, "Customer", self.customer_var, 0, 1,[])
        self._add_combo(form_card, "Order Status", self.order_status_var, 0, 2, self.valid_statuses)

        self._add_entry(form_card, "Order Date", self.order_date_var, 1, 0, state="readonly")
        self._add_entry(form_card, "Total Amount", self.total_amount_var, 1, 1, state="readonly")

        button_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        button_frame.grid(row=2, column=0, columnspan=3, padx=18, pady=(6, 18), sticky="ew")

        add_button = ctk.CTkButton(
            button_frame,
            text="Add Order",
            width=120,
            height=40,
            corner_radius=10,
            command=self.add_order
        )
        add_button.grid(row=0, column=0, padx=(0, 10))

        update_button = ctk.CTkButton(
            button_frame,
            text="Update Status",
            width=130,
            height=40,
            corner_radius=10,
            fg_color="#0F766E",
            hover_color="#115E59",
            command=self.update_order_status
        )
        update_button.grid(row=0, column=1, padx=(0, 10))

        delete_button = ctk.CTkButton(
            button_frame,
            text="Delete Order",
            width=130,
            height=40,
            corner_radius=10,
            fg_color="#B91C1C",
            hover_color="#991B1B",
            command=self.delete_order
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

    def _add_combo(self, master, label, variable, row, column, values):
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
            height=38,
            state="readonly",
            values=values
        )
        combo.grid(row=1, column=0, sticky="ew")

        if label == "Customer":
            self.customer_combo = combo
        else:
            self.status_combo = combo

    def _build_table(self):
        table_card = ctk.CTkFrame(
            self,
            fg_color="#1F2937",
            corner_radius=20,
            border_width=1,
            border_color="#334155"
    
        )

        table_card.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(0, weight=1)
        table_card.grid_propagate(False)
        table_card.configure(height=700)

        setup_table_style()

        table_frame = tk.Frame(table_card, bg="#1F2937", highlightthickness=0)
        table_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(table_frame, columns=self.columns, show="headings")

        headings = {
            "order_id": "Order ID",
            "customer_id": "Customer ID",
            "customer_name": "Customer",
            "order_date": "Order Date",
            "total_amount": "Total Amount",
            "order_status": "Status",
        }

        widths = {
            "order_id": 90,
            "customer_id": 100,
            "customer_name": 220,
            "order_date": 180,
            "total_amount": 120,
            "order_status": 130,
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
        self.search_orders()

    def _load_customers(self):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT CustomerID, FirstName, LastName
                FROM Customers
                ORDER BY FirstName, LastName, CustomerID
                """
            )
            customers = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

        self.customer_map = {
            f"{row.CustomerID} - {row.FirstName} {row.LastName or ''}".strip(): row.CustomerID
            for row in customers
        }

        customer_values = list(self.customer_map.keys())
        self.customer_combo.configure(values=customer_values)

        if customer_values:
            self.customer_var.set(customer_values[0])
        else:
            self.customer_var.set("")

        if self.valid_statuses:
            self.order_status_var.set(self.valid_statuses[0])

    def _fetch_orders(self, order_id=None):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            query = """
                SELECT
                    O.OrderID,
                    O.CustomerID,
                    C.FirstName,
                    C.LastName,
                    O.OrderDate,
                    O.TotalAmount,
                    O.OrderStatus
                FROM Orders AS O
                INNER JOIN Customers AS C
                    ON O.CustomerID = C.CustomerID
            """

            params = None

            if order_id is not None:
                query += " WHERE O.OrderID = ?"
                params = (order_id,)

            query += " ORDER BY O.OrderID"

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

        for order in rows:
            customer_name = f"{order.FirstName} {order.LastName or ''}".strip()
            self.tree.insert(
                "",
                "end",
                values=(
                    order.OrderID,
                    order.CustomerID,
                    customer_name,
                    str(order.OrderDate or ""),
                    f"Rs {order.TotalAmount}",
                    order.OrderStatus,
                )
            )

    def _selected_customer_id(self):
        customer_label = self.customer_var.get().strip()
        customer_id = self.customer_map.get(customer_label)

        if customer_id is None:
            raise ValueError("Select a valid customer.")

        return customer_id

    def on_row_select(self, _event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")

        self.order_id_var.set(values[0])
        self.order_date_var.set(values[3])
        self.total_amount_var.set(str(values[4]).replace("Rs ", ""))
        self.order_status_var.set(values[5])

        customer_id = values[1]
        customer_name = values[2]
        label = f"{customer_id} - {customer_name}"
        if label in self.customer_map:
            self.customer_var.set(label)

    def clear_form(self):
        self.order_id_var.set("")
        self.order_date_var.set("")
        self.total_amount_var.set("")
        self.search_var.set("")

        if self.customer_map:
            self.customer_var.set(list(self.customer_map.keys())[0])
        else:
            self.customer_var.set("")

        if self.valid_statuses:
            self.order_status_var.set(self.valid_statuses[0])
        else:
            self.order_status_var.set("")

        for selected in self.tree.selection():
            self.tree.selection_remove(selected)

        self.summary_var.set("Form cleared")

    def refresh_page(self):
        self._load_customers()
        self.load_orders()
        self.clear_form()

    def load_orders(self):
        try:
            rows = self._fetch_orders()
            self._populate_table(rows)
            self.summary_var.set(f"{len(rows)} orders loaded from the database")
        except Exception as error:
            self._populate_table([])
            self.summary_var.set(f"Failed to load orders: {error}")

    def search_orders(self):
        search_text = self.search_var.get().strip()

        try:
            if search_text:
                order_id = int(search_text)
                rows = self._fetch_orders(order_id)
                self.summary_var.set(f"{len(rows)} matching orders for ID {order_id}")
            else:
                rows = self._fetch_orders()
                self.summary_var.set(f"{len(rows)} orders loaded from the database")

            self._populate_table(rows)
        except ValueError:
            self._populate_table([])
            self.summary_var.set("Search failed: Order ID must be numeric.")
        except Exception as error:
            self._populate_table([])
            self.summary_var.set(f"Search failed: {error}")

    def add_order(self):
        conn = None
        cursor = None

        try:
            customer_id = self._selected_customer_id()
            order_status = self.order_status_var.get().strip().title()

            if order_status not in self.valid_statuses:
                raise ValueError("Select a valid order status.")

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO Orders
                (
                    CustomerID,
                    TotalAmount,
                    OrderStatus
                )
                VALUES (?, ?, ?)
                """,
                (
                    customer_id,
                    0,
                    order_status,
                )
            )

            conn.commit()

            self.load_orders()
            self.clear_form()
            self.summary_var.set("Order created successfully")
            messagebox.showinfo(
                "Success",
                "Order created successfully.\nTotal amount is initialized to 0.\nAdd products using Order Item Management."
            )
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))
        except pyodbc.IntegrityError as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Could not add order.\n\n{error}")
        except Exception as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Unexpected Error", str(error))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_order_status(self):
        conn = None
        cursor = None

        try:
            order_id = self.order_id_var.get().strip()
            if not order_id:
                raise ValueError("Select an order from the table to update.")

            status = self.order_status_var.get().strip().title()
            if status not in self.valid_statuses:
                raise ValueError("Select a valid order status.")

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE Orders
                SET OrderStatus = ?
                WHERE OrderID = ?
                """,
                (
                    status,
                    int(order_id),
                )
            )

            if cursor.rowcount == 0:
                raise ValueError("Order not found.")

            conn.commit()

            self.load_orders()
            self.summary_var.set(f"Order {order_id} updated successfully")
            messagebox.showinfo("Success", "Order status updated successfully.")
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))
        except Exception as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Unexpected Error", str(error))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_order(self):
        conn = None
        cursor = None

        try:
            order_id = self.order_id_var.get().strip()
            if not order_id:
                raise ValueError("Select an order from the table to delete.")

            confirmed = messagebox.askyesno(
                "Confirm Delete",
                f"Delete order ID {order_id}?"
            )

            if not confirmed:
                return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM Orders
                WHERE OrderID = ?
                """,
                (int(order_id),)
            )

            if cursor.rowcount == 0:
                raise ValueError("Order not found.")

            conn.commit()

            self.load_orders()
            self.clear_form()
            self.summary_var.set(f"Order {order_id} deleted successfully")
            messagebox.showinfo("Success", "Order deleted successfully.")
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))
        except pyodbc.IntegrityError as error:
            if conn:
                conn.rollback()
            messagebox.showerror(
                "Database Error",
                "Could not delete order. The order may still contain order items.\n\n"
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
