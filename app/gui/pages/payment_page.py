import tkinter as tk
from tkinter import messagebox, ttk

import customtkinter as ctk
import pyodbc

from database import get_connection
from gui.widgets.table_style import setup_table_style


class PaymentPage(ctk.CTkFrame):
    columns = (
        "payment_id",
        "order_id",
        "customer_name",
        "payment_date",
        "payment_method",
        "amount",
        "payment_status",
        "transaction_reference",
    )

    valid_methods = ["Cash", "Card", "UPI", "Net Banking"]
    valid_statuses = ["Pending", "Completed", "Failed", "Refunded"]

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.search_var = tk.StringVar()
        self.summary_var = tk.StringVar(value="Loading payments...")

        self.payment_id_var = tk.StringVar()
        self.order_var = tk.StringVar()
        self.payment_date_var = tk.StringVar()
        self.payment_method_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.payment_status_var = tk.StringVar()
        self.transaction_reference_var = tk.StringVar()

        self.order_map = {}
        self.order_totals = {}
        self.payment_window = None
        self.payment_tree = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_header()
        self._load_orders()
        self.load_payments(update_window=False)

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
            text="Payments",
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
            placeholder_text="Search by payment ID"
        )
        self.search_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.search_entry.bind("<Return>", self._on_search_enter)

        ctk.CTkButton(
            search_frame,
            text="Search",
            width=90,
            height=38,
            corner_radius=10,
            command=self.search_payments
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

        self._add_entry(form_card, "Payment ID", self.payment_id_var, 0, 0, state="readonly")
        self._add_entry(form_card, "Payment Date", self.payment_date_var, 0, 1, state="readonly")

        self._add_combo(form_card, "Order", self.order_var, 1, 0, [])
        self._add_combo(form_card, "Payment Method", self.payment_method_var, 1, 1, self.valid_methods)

        self._add_entry(form_card, "Amount", self.amount_var, 2, 0)
        self._add_combo(form_card, "Payment Status", self.payment_status_var, 2, 1, self.valid_statuses)

        self._add_entry(
            form_card,
            "Transaction Reference",
            self.transaction_reference_var,
            3,
            0,
            columnspan=2
        )

        button_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        button_frame.grid(row=4, column=0, columnspan=2, padx=12, pady=(2, 12), sticky="ew")
        for column in range(5):
            button_frame.grid_columnconfigure(column, weight=1)

        ctk.CTkButton(
            button_frame,
            text="View Payments",
            width=110,
            height=40,
            corner_radius=10,
            fg_color="#334155",
            hover_color="#475569",
            command=self.open_payment_window
        ).grid(row=0, column=0, padx=6, sticky="ew")

        ctk.CTkButton(
            button_frame,
            text="Add Payment",
            width=110,
            height=40,
            corner_radius=10,
            command=self.add_payment
        ).grid(row=0, column=1, padx=6, sticky="ew")

        ctk.CTkButton(
            button_frame,
            text="Update",
            width=120,
            height=40,
            corner_radius=10,
            fg_color="#0F766E",
            hover_color="#115E59",
            command=self.update_payment
        ).grid(row=0, column=2, padx=6, sticky="ew")

        ctk.CTkButton(
            button_frame,
            text="Delete",
            width=120,
            height=40,
            corner_radius=10,
            fg_color="#B91C1C",
            hover_color="#991B1B",
            command=self.delete_payment
        ).grid(row=0, column=3, padx=6, sticky="ew")

        ctk.CTkButton(
            button_frame,
            text="Clear Form",
            width=105,
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

    def _add_combo(self, master, label, variable, row, column, values):
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
            values=values
        )
        combo.grid(row=1, column=0, sticky="ew")

        if label == "Order":
            self.order_combo = combo
        elif label == "Payment Method":
            self.method_combo = combo
        else:
            self.status_combo = combo

    def _build_payment_window(self):
        if self.payment_window is not None and self.payment_window.winfo_exists():
            self.payment_window.focus()
            return

        self.payment_window = ctk.CTkToplevel(self)
        self.payment_window.title("Payments")
        self.payment_window.geometry("1100x520")
        self.payment_window.minsize(950, 420)
        self.payment_window.configure(fg_color="#111827")
        self.payment_window.grid_columnconfigure(0, weight=1)
        self.payment_window.grid_rowconfigure(0, weight=1)
        self.payment_window.protocol("WM_DELETE_WINDOW", self._close_payment_window)

        table_card = ctk.CTkFrame(
            self.payment_window,
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
            text="Payments",
            font=("Segoe UI", 24, "bold"),
            text_color="white"
        ).grid(row=0, column=0, padx=18, pady=(16, 10), sticky="w")

        setup_table_style()

        table_frame = tk.Frame(table_card, bg="#1F2937", highlightthickness=0)
        table_frame.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        self.payment_tree = ttk.Treeview(table_frame, columns=self.columns, show="headings")
        self.payment_tree.configure(height=18)

        headings = {
            "payment_id": "Payment ID",
            "order_id": "Order ID",
            "customer_name": "Customer",
            "payment_date": "Payment Date",
            "payment_method": "Method",
            "amount": "Amount",
            "payment_status": "Status",
            "transaction_reference": "Reference",
        }

        widths = {
            "payment_id": 100,
            "order_id": 90,
            "customer_name": 220,
            "payment_date": 180,
            "payment_method": 120,
            "amount": 110,
            "payment_status": 120,
            "transaction_reference": 240,
        }

        for column in self.columns:
            self.payment_tree.heading(column, text=headings[column])
            self.payment_tree.column(column, width=widths[column], anchor="w", stretch=True)

        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.payment_tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.payment_tree.xview)

        self.payment_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        self.payment_tree.bind("<<TreeviewSelect>>", self.on_row_select)

        self.payment_tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

    def _close_payment_window(self):
        if self.payment_window is not None and self.payment_window.winfo_exists():
            self.payment_window.destroy()
        self.payment_window = None
        self.payment_tree = None

    def open_payment_window(self):
        self._build_payment_window()
        self.load_payments(update_window=True)

    def _on_search_enter(self, _event):
        self.search_payments()

    def _load_orders(self):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    O.OrderID,
                    O.TotalAmount,
                    C.FirstName,
                    C.LastName
                FROM Orders AS O
                INNER JOIN Customers AS C
                    ON O.CustomerID = C.CustomerID
                ORDER BY O.OrderID
                """
            )
            orders = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

        self.order_map = {
            f"{row.OrderID} - {row.FirstName} {row.LastName or ''}".strip(): row.OrderID
            for row in orders
        }
        self.order_totals = {
            row.OrderID: float(row.TotalAmount or 0)
            for row in orders
        }

        order_values = list(self.order_map.keys())
        self.order_combo.configure(values=order_values)

        self.order_var.set(order_values[0] if order_values else "")
        self.payment_method_var.set(self.valid_methods[0] if self.valid_methods else "")
        self.payment_status_var.set(self.valid_statuses[0] if self.valid_statuses else "")

    def _fetch_payments(self, payment_id=None):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            query = """
                SELECT
                    P.PaymentID,
                    P.OrderID,
                    C.FirstName,
                    C.LastName,
                    P.PaymentDate,
                    P.PaymentMethod,
                    P.Amount,
                    P.PaymentStatus,
                    P.TransactionReference
                FROM Payments AS P
                INNER JOIN Orders AS O
                    ON P.OrderID = O.OrderID
                INNER JOIN Customers AS C
                    ON O.CustomerID = C.CustomerID
            """

            params = None
            if payment_id is not None:
                query += " WHERE P.PaymentID = ?"
                params = (payment_id,)

            query += " ORDER BY P.PaymentID"

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def _populate_table(self, rows):
        if self.payment_tree is None or not self.payment_tree.winfo_exists():
            return

        for item in self.payment_tree.get_children():
            self.payment_tree.delete(item)

        for payment in rows:
            customer_name = f"{payment.FirstName} {payment.LastName or ''}".strip()
            self.payment_tree.insert(
                "",
                "end",
                values=(
                    payment.PaymentID,
                    payment.OrderID,
                    customer_name,
                    str(payment.PaymentDate or ""),
                    payment.PaymentMethod,
                    f"{float(payment.Amount):.2f}",
                    payment.PaymentStatus,
                    payment.TransactionReference or "",
                )
            )

    def _selected_order_id(self):
        order_id = self.order_map.get(self.order_var.get().strip())
        if order_id is None:
            raise ValueError("Select a valid order.")
        return order_id

    def _parse_amount(self, order_id):
        try:
            amount = float(self.amount_var.get().strip())
        except ValueError as error:
            raise ValueError("Amount must be numeric.") from error

        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")

        order_total = self.order_totals.get(order_id, 0)
        if amount > order_total:
            raise ValueError(f"Payment exceeds order total of {order_total:.2f}.")

        return amount

    def _validate_method(self):
        payment_method = self.payment_method_var.get().strip()
        if payment_method not in self.valid_methods:
            raise ValueError("Select a valid payment method.")
        return payment_method

    def _validate_status(self):
        payment_status = self.payment_status_var.get().strip().title()
        if payment_status == "Upi":
            payment_status = "UPI"
        if payment_status not in self.valid_statuses:
            raise ValueError("Select a valid payment status.")
        return payment_status

    def on_row_select(self, event):
        selected = event.widget.selection()
        if not selected:
            return

        values = event.widget.item(selected[0], "values")

        self.payment_id_var.set(values[0])
        self.payment_date_var.set(values[3])
        self.payment_method_var.set(values[4])
        self.amount_var.set(values[5])
        self.payment_status_var.set(values[6])
        self.transaction_reference_var.set(values[7])

        order_label = f"{values[1]} - {values[2]}"
        if order_label in self.order_map:
            self.order_var.set(order_label)

    def clear_form(self):
        self.payment_id_var.set("")
        self.payment_date_var.set("")
        self.amount_var.set("")
        self.transaction_reference_var.set("")
        self.search_var.set("")

        order_values = list(self.order_map.keys())
        self.order_var.set(order_values[0] if order_values else "")
        self.payment_method_var.set(self.valid_methods[0] if self.valid_methods else "")
        self.payment_status_var.set(self.valid_statuses[0] if self.valid_statuses else "")

        if self.payment_tree is not None and self.payment_tree.winfo_exists():
            for selected in self.payment_tree.selection():
                self.payment_tree.selection_remove(selected)

        self.summary_var.set("Form cleared")

    def refresh_page(self):
        self._load_orders()
        self.load_payments(update_window=True)
        self.clear_form()

    def load_payments(self, update_window=True):
        try:
            rows = self._fetch_payments()
            if update_window:
                self._populate_table(rows)
            self.summary_var.set(f"{len(rows)} payments loaded from the database")
        except Exception as error:
            if update_window:
                self._populate_table([])
            self.summary_var.set(f"Failed to load payments: {error}")

    def search_payments(self):
        search_text = self.search_var.get().strip()

        try:
            if search_text:
                payment_id = int(search_text)
                rows = self._fetch_payments(payment_id)
                self.summary_var.set(f"{len(rows)} matching payments for ID {payment_id}")
            else:
                rows = self._fetch_payments()
                self.summary_var.set(f"{len(rows)} payments loaded from the database")

            self.open_payment_window()
            self._populate_table(rows)
        except ValueError:
            self.summary_var.set("Search failed: Payment ID must be numeric.")
        except Exception as error:
            self.summary_var.set(f"Search failed: {error}")

    def add_payment(self):
        conn = None
        cursor = None

        try:
            order_id = self._selected_order_id()
            payment_method = self._validate_method()
            amount = self._parse_amount(order_id)
            payment_status = self._validate_status()
            transaction_reference = self.transaction_reference_var.get().strip() or None

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO Payments
                (
                    OrderID,
                    PaymentMethod,
                    Amount,
                    PaymentStatus,
                    TransactionReference
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    order_id,
                    payment_method,
                    amount,
                    payment_status,
                    transaction_reference,
                )
            )

            conn.commit()

            self.load_payments()
            self.clear_form()
            self.summary_var.set(f"Payment added for order {order_id}")
            messagebox.showinfo("Success", "Payment added successfully.")
        except ValueError as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Invalid Input", str(error))
        except pyodbc.IntegrityError as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Could not add payment.\n\n{error}")
        except Exception as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Unexpected Error", str(error))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_payment(self):
        conn = None
        cursor = None

        try:
            payment_id = self.payment_id_var.get().strip()
            if not payment_id:
                raise ValueError("Select a payment from the table to update.")

            order_id = self._selected_order_id()
            payment_method = self._validate_method()
            amount = self._parse_amount(order_id)
            payment_status = self._validate_status()
            transaction_reference = self.transaction_reference_var.get().strip() or None

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE Payments
                SET
                    OrderID = ?,
                    PaymentMethod = ?,
                    Amount = ?,
                    PaymentStatus = ?,
                    TransactionReference = ?
                WHERE PaymentID = ?
                """,
                (
                    order_id,
                    payment_method,
                    amount,
                    payment_status,
                    transaction_reference,
                    int(payment_id),
                )
            )

            if cursor.rowcount == 0:
                raise ValueError("Payment not found.")

            conn.commit()

            self.load_payments()
            self.summary_var.set(f"Payment {payment_id} updated successfully")
            messagebox.showinfo("Success", "Payment updated successfully.")
        except ValueError as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Invalid Input", str(error))
        except pyodbc.IntegrityError as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Could not update payment.\n\n{error}")
        except Exception as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Unexpected Error", str(error))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_payment(self):
        conn = None
        cursor = None

        try:
            payment_id = self.payment_id_var.get().strip()
            if not payment_id:
                raise ValueError("Select a payment from the table to delete.")

            confirmed = messagebox.askyesno(
                "Confirm Delete",
                f"Delete payment ID {payment_id}?"
            )
            if not confirmed:
                return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM Payments
                WHERE PaymentID = ?
                """,
                (int(payment_id),)
            )

            if cursor.rowcount == 0:
                raise ValueError("Payment not found.")

            conn.commit()

            self.load_payments()
            self.clear_form()
            self.summary_var.set(f"Payment {payment_id} deleted successfully")
            messagebox.showinfo("Success", "Payment deleted successfully.")
        except ValueError as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Invalid Input", str(error))
        except pyodbc.IntegrityError as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Could not delete payment.\n\n{error}")
        except Exception as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Unexpected Error", str(error))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
