import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
    MENU_ITEMS = [
        ("products", "Product"),
        ("customers", "Customer"),
        ("suppliers", "Supplier"),
        ("categories", "Category"),
        ("inventory", "Inventory"),
        ("orders", "Orders"),
        ("orderitems", "OrderItem"),
        ("payments", "Payment"),
        ("reports", "Reports"),
        ("analytics", "Data Analytics"),
        ("dashboard", "Dashboard"),
    ]

    def __init__(self, master):
        super().__init__(
            master,
            width=300,
            corner_radius=0,
            fg_color="#1F2937"
        )

        self.grid_propagate(False)
        self.buttons = {}
        self._build_buttons()
        self._build_footer()

        self.highlight_button("dashboard")


    def _build_buttons(self):
        for key, text in self.MENU_ITEMS:
            button = ctk.CTkButton(
                self,
                text=text,
                width=250,
                height=46,
                corner_radius=12,
                fg_color="transparent",
                hover_color="#2563EB",
                text_color="white",
                anchor="w",
                font=("Segoe UI", 15),
                command=lambda menu_key=key: self.on_click(menu_key)
            )
            button.pack(
                padx=20,
                pady=5,
                fill="x"
            )
            self.buttons[key] = button

    def _build_footer(self):
        bottom = ctk.CTkLabel(
            self,
            text="ShopSync 2026",
            font=("Segoe UI", 11),
            text_color="#6B7280"
        )
        bottom.pack(side="bottom", pady=18)

    def highlight_button(self, selected):
        for key, button in self.buttons.items():
            if key == selected:
                button.configure(
                    fg_color="#2563EB",
                    hover_color="#2563EB",
                    text_color="white"
                )
            else:
                button.configure(
                    fg_color="transparent",
                    hover_color="#374151",
                    text_color="#D1D5DB"
                )

    def on_click(self, key):
        self.highlight_button(key)

        if key == "dashboard":
            self.master.show_dashboard()
        elif key == "products":
            self.master.show_products()
        elif key == "customers":
            self.master.show_customers()
        elif key == "suppliers":
            self.master.show_suppliers()
        elif key == "categories":
            self.master.show_categories()
        elif key == "inventory":
            self.master.show_inventory()
        elif key == "orders":
            self.master.show_orders()
        elif key == "orderitems":
            self.master.show_orderitems()
        elif key == "payments":
            self.master.show_payments()
        elif key == "reports":
            self.master.show_reports()
        elif key == "analytics":
            self.master.show_analytics()
