import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from services.auth_service import authenticate, ensure_users_table


class LoginWindow(ctk.CTk):
    """Desktop sign-in window shown before the ShopSync dashboard."""

    def __init__(self, on_login):
        super().__init__()
        self.on_login = on_login
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Sign in to continue")

        self.title("ShopSync | Sign in")
        self.geometry("480x500")
        self.resizable(False, False)
        self.configure(fg_color="#111827")
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self._build()
        self.after(100, self._prepare_authentication)

    def _build(self):
        card = ctk.CTkFrame(self, fg_color="#1F2937", corner_radius=20, border_width=1, border_color="#334155")
        card.pack(fill="both", expand=True, padx=38, pady=38)

        ctk.CTkLabel(card, text="ShopSync", font=("Segoe UI", 32, "bold"), text_color="white").pack(pady=(46, 4))
        ctk.CTkLabel(card, text="Inventory Management", font=("Segoe UI", 15), text_color="#94A3B8").pack(pady=(0, 32))
        self._field(card, "Username", self.username_var, False)
        self._field(card, "Password", self.password_var, True)
        ctk.CTkButton(card, text="Sign In", height=44, corner_radius=10, command=self._sign_in).pack(fill="x", padx=45, pady=(24, 12))
        ctk.CTkLabel(card, textvariable=self.status_var, font=("Segoe UI", 12), text_color="#CBD5E1", wraplength=330).pack(padx=30)
        self.bind("<Return>", lambda _event: self._sign_in())

    @staticmethod
    def _field(master, label, variable, masked):
        ctk.CTkLabel(master, text=label, font=("Segoe UI", 13, "bold"), text_color="#CBD5E1").pack(anchor="w", padx=45, pady=(9, 5))
        ctk.CTkEntry(master, textvariable=variable, height=38, show="*" if masked else "").pack(fill="x", padx=45)

    def _prepare_authentication(self):
        try:
            ensure_users_table()
            self.status_var.set("Sign in to continue")
        except Exception as error:
            self.status_var.set("Database connection could not be prepared.")
            messagebox.showerror("Database error", f"Unable to prepare authentication.\n\n{error}")

    def _sign_in(self):
        try:
            user = authenticate(self.username_var.get(), self.password_var.get())
        except Exception as error:
            messagebox.showerror("Sign in failed", f"Unable to contact the database.\n\n{error}")
            return
        if not user:
            self.password_var.set("")
            self.status_var.set("Invalid username or password.")
            return
        self.destroy()
        self.on_login(user)
