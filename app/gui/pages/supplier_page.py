import tkinter as tk
from tkinter import messagebox, ttk

import customtkinter as ctk
import pyodbc

from database import get_connection
from gui.widgets.table_style import setup_table_style


class SupplierPage(ctk.CTkFrame):
    columns = (
        "id",
        "supplier_name",
        "contact_person",
        "phone",
        "email",
        "address",
    )

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.search_var = tk.StringVar()
        self.summary_var = tk.StringVar(value="Loading suppliers...")

        self.supplier_id_var = tk.StringVar()
        self.supplier_name_var = tk.StringVar()
        self.contact_person_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_table()
        self.load_suppliers()

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
            text="Suppliers",
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
            placeholder_text="Search by supplier name"
        )
        self.search_entry.grid(row=0, column=0, padx=(0, 10))
        self.search_entry.bind("<Return>", self._on_search_enter)

        search_button = ctk.CTkButton(
            search_frame,
            text="Search",
            width=90,
            height=34,
            corner_radius=10,
            command=self.search_suppliers
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
        form_card.grid_columnconfigure((0, 1, 2), weight=1)

        self._add_entry(form_card, "Supplier ID", self.supplier_id_var, 0, 0, state="readonly")
        self._add_entry(form_card, "Supplier Name", self.supplier_name_var, 0, 1)
        self._add_entry(form_card, "Contact Person", self.contact_person_var, 0, 2)

        self._add_entry(form_card, "Phone", self.phone_var, 1, 0)
        self._add_entry(form_card, "Email", self.email_var, 1, 1)
        self._add_entry(form_card, "Address", self.address_var, 1, 2)

        button_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        button_frame.grid(row=2, column=0, columnspan=3, padx=18, pady=(4, 10), sticky="ew")

        add_button = ctk.CTkButton(
            button_frame,
            text="Add Supplier",
            width=120,
            height=34,
            corner_radius=10,
            command=self.add_supplier
        )
        add_button.grid(row=0, column=0, padx=(0, 10))

        update_button = ctk.CTkButton(
            button_frame,
            text="Update Supplier",
            width=130,
            height=34,
            corner_radius=10,
            fg_color="#0F766E",
            hover_color="#115E59",
            command=self.update_supplier
        )
        update_button.grid(row=0, column=1, padx=(0, 10))

        delete_button = ctk.CTkButton(
            button_frame,
            text="Delete Supplier",
            width=130,
            height=34,
            corner_radius=10,
            fg_color="#B91C1C",
            hover_color="#991B1B",
            command=self.delete_supplier
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
            height=38,
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
        table_card.grid(row=1, column=0, padx=20, pady=(5, 24), sticky="nsew")
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
            "supplier_name": "Supplier",
            "contact_person": "Contact Person",
            "phone": "Phone",
            "email": "Email",
            "address": "Address",
        }

        widths = {
            "id": 70,
            "supplier_name": 190,
            "contact_person": 180,
            "phone": 140,
            "email": 240,
            "address": 350,
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
        self.search_suppliers()

    def _fetch_suppliers(self, supplier_name=None):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            query = """
                SELECT
                    SupplierID,
                    SupplierName,
                    ContactPerson,
                    Phone,
                    Email,
                    Address
                FROM Suppliers
            """

            params = None

            if supplier_name:
                query += " WHERE SupplierName LIKE ?"
                params = (f"%{supplier_name}%",)

            query += " ORDER BY SupplierID"

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

        for supplier in rows:
            self.tree.insert(
                "",
                "end",
                values=(
                    supplier.SupplierID,
                    supplier.SupplierName,
                    supplier.ContactPerson or "",
                    supplier.Phone or "",
                    supplier.Email or "",
                    supplier.Address or "",
                )
            )

    def _parse_form_values(self):
        supplier_name = self.supplier_name_var.get().strip()
        contact_person = self.contact_person_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_var.get().strip()

        if not supplier_name.replace(" ", "").isalpha():
            raise ValueError("Supplier name should contain only letters.")

        if not contact_person.replace(" ", "").isalpha():
            raise ValueError("Contact person should contain only letters.")

        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")

        if "@" not in email or "." not in email:
            raise ValueError("Invalid email address.")

        if not address:
            raise ValueError("Address cannot be empty.")

        return (
            supplier_name,
            contact_person,
            phone,
            email,
            address,
        )

    def on_row_select(self, _event):
        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(selected[0], "values")

        self.supplier_id_var.set(values[0])
        self.supplier_name_var.set(values[1])
        self.contact_person_var.set(values[2])
        self.phone_var.set(values[3])
        self.email_var.set(values[4])
        self.address_var.set(values[5])

    def clear_form(self):
        self.supplier_id_var.set("")
        self.supplier_name_var.set("")
        self.contact_person_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.address_var.set("")
        self.search_var.set("")

        for selected in self.tree.selection():
            self.tree.selection_remove(selected)

        self.summary_var.set("Form cleared")

    def refresh_page(self):
        self.load_suppliers()
        self.clear_form()

    def load_suppliers(self):
        try:
            rows = self._fetch_suppliers()
            self._populate_table(rows)
            self.summary_var.set(f"{len(rows)} suppliers loaded from the database")
        except Exception as error:
            self._populate_table([])
            self.summary_var.set(f"Failed to load suppliers: {error}")

    def search_suppliers(self):
        search_text = self.search_var.get().strip()

        try:
            rows = self._fetch_suppliers(search_text if search_text else None)
            self._populate_table(rows)

            if search_text:
                self.summary_var.set(
                    f"{len(rows)} matching suppliers for '{search_text}'"
                )
            else:
                self.summary_var.set(f"{len(rows)} suppliers loaded from the database")
        except Exception as error:
            self._populate_table([])
            self.summary_var.set(f"Search failed: {error}")

    def add_supplier(self):
        conn = None
        cursor = None

        try:
            values = self._parse_form_values()

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO Suppliers
                (
                    SupplierName,
                    ContactPerson,
                    Phone,
                    Email,
                    Address
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                values
            )

            conn.commit()

            self.load_suppliers()
            self.clear_form()
            self.summary_var.set("Supplier added successfully")
            messagebox.showinfo("Success", "Supplier added successfully.")
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))
        except pyodbc.IntegrityError as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Could not add supplier.\n\n{error}")
        except Exception as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Unexpected Error", str(error))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_supplier(self):
        conn = None
        cursor = None

        try:
            supplier_id = self.supplier_id_var.get().strip()

            if not supplier_id:
                raise ValueError("Select a supplier from the table to update.")

            values = self._parse_form_values()

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE Suppliers
                SET
                    SupplierName = ?,
                    ContactPerson = ?,
                    Phone = ?,
                    Email = ?,
                    Address = ?
                WHERE SupplierID = ?
                """,
                values + (int(supplier_id),)
            )

            if cursor.rowcount == 0:
                raise ValueError("Supplier not found.")

            conn.commit()

            self.load_suppliers()
            self.summary_var.set(f"Supplier {supplier_id} updated successfully")
            messagebox.showinfo("Success", "Supplier updated successfully.")
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))
        except pyodbc.IntegrityError as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Could not update supplier.\n\n{error}")
        except Exception as error:
            if conn:
                conn.rollback()
            messagebox.showerror("Unexpected Error", str(error))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_supplier(self):
        conn = None
        cursor = None

        try:
            supplier_id = self.supplier_id_var.get().strip()

            if not supplier_id:
                raise ValueError("Select a supplier from the table to delete.")

            confirmed = messagebox.askyesno(
                "Confirm Delete",
                f"Delete supplier ID {supplier_id}?"
            )

            if not confirmed:
                return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM Suppliers
                WHERE SupplierID = ?
                """,
                (int(supplier_id),)
            )

            if cursor.rowcount == 0:
                raise ValueError("Supplier not found.")

            conn.commit()

            self.load_suppliers()
            self.clear_form()
            self.summary_var.set(f"Supplier {supplier_id} deleted successfully")
            messagebox.showinfo("Success", "Supplier deleted successfully.")
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))
        except pyodbc.IntegrityError as error:
            if conn:
                conn.rollback()
            messagebox.showerror(
                "Database Error",
                "Could not delete supplier. The supplier may still be linked to products.\n\n"
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
