import customtkinter as ctk

from gui.dashboard_frame import DashboardFrame
from gui.pages.category_page import CategoryPage
from gui.pages.customer_page import CustomerPage
from gui.pages.inventory_page import InventoryPage
from gui.pages.order_page import OrderPage
from gui.pages.orderitem_page import OrderItemPage
from gui.pages.payment_page import PaymentPage
from gui.pages.product_page import ProductPage
from gui.pages.report_page import ReportPage
from gui.pages.supplier_page import SupplierPage
from gui.sidebar import Sidebar


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class PlaceholderPage(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        card = ctk.CTkFrame(
            self,
            fg_color="#1F2937",
            corner_radius=20,
            border_width=1,
            border_color="#334155"
        )
        card.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)

        heading = ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 30, "bold"),
            text_color="white"
        )
        heading.pack(anchor="w", padx=28, pady=(28, 10))

        message = ctk.CTkLabel(
            card,
            text="The GUI shell is ready. This module will be wired to the existing backend next.",
            font=("Segoe UI", 16),
            text_color="#CBD5E1"
        )
        message.pack(anchor="w", padx=28, pady=(0, 28))


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.current_page = None
        self.page_config = {
            "products": {
                "title": "1. Product Management",
                "page": ProductPage,
                "status": "Product Management loaded",
            },
            "customers": {
                "title": "2. Customer Management",
                "page": CustomerPage,
                "status": "Customer Management loaded",
            },
            "suppliers": {
                "title": "3. Supplier Management",
                "page": SupplierPage,
                "status": "Supplier Management loaded",
            },
            "categories": {
                "title": "4. Category Management",
                "page": CategoryPage,
                "status": "Category Management loaded",
            },
            "inventory": {
                "title": "5. Inventory Management",
                "page": InventoryPage,
                "status": "Inventory Management loaded",
            },
            "orders": {
                "title": "6. Order Management",
                "page": OrderPage,
                "status": "Order Management loaded",
            },
            "orderitems": {
                "title": "7. OrderItem Management",
                "page": OrderItemPage,
                "status": "OrderItem Management loaded",
            },
            "payments": {
                "title": "8. Payment Management",
                "page": PaymentPage,
                "status": "Payment Management loaded",
            },
            "reports": {
                "title": "9. Report",
                "page": ReportPage,
                "status": "Report page loaded",
            },
            "dashboard": {
                "title": "10. Dashboard",
                "page": DashboardFrame,
                "status": "Dashboard loaded",
            },
        }

        self.title("ShopSync")
        self.geometry("1450x850")
        self.minsize(1300, 760)
        self.configure(fg_color="#111827")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_sidebar()
        self._build_content()
        self._build_status_bar()

        self.show_dashboard()

    def _build_header(self):
        self.header = ctk.CTkFrame(
            self,
            height=50,
            fg_color="#1E293B",
            corner_radius=0
        )
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid_columnconfigure(1, weight=1)

        self.logo = ctk.CTkLabel(
            self.header,
            text="ShopSync",
            font=("Segoe UI", 20, "bold"),
            text_color="white"
        )
        self.logo.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.subtitle = ctk.CTkLabel(
            self.header,
            font=("Segoe UI", 10),
            text_color="#CBD5E1"
        )
        self.subtitle.grid(row=0, column=1, padx=20, pady= 10, sticky="e")

    def _build_sidebar(self):
        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=1, column=0, sticky="ns")

    def _build_content(self):
        self.content = ctk.CTkFrame(
            self,
            fg_color="#181F2A",
            corner_radius=18,
            border_width=1,
            border_color="#2D3748"
        )
        self.content.grid(row=1, column=1, padx=25, pady=25, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

    def _build_status_bar(self):
        self.status = ctk.CTkFrame(
            self,
            height=34,
            fg_color="#1E293B",
            corner_radius=0
        )
        self.status.grid(row=2, column=0, columnspan=2, sticky="ew")
        self.status.grid_columnconfigure(0, weight=1)
        self.status.grid_columnconfigure(1, weight=1)

        self.status_label = ctk.CTkLabel(
            self.status,
            text="Ready",
            font=("Segoe UI", 13),
            text_color="#86EFAC"
        )
        self.status_label.grid(row=0, column=0, padx=20, pady=6, sticky="w")

        version = ctk.CTkLabel(
            self.status,
            text="Version 1.0",
            font=("Segoe UI", 12),
            text_color="#94A3B8"
        )
        version.grid(row=0, column=1, padx=20, sticky="e")

    def clear_page(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self.current_page = None

    def set_status(self, message, color="#86EFAC"):
        self.status_label.configure(text=message, text_color=color)

    def show_page(self, page_class, status_message, *args, **kwargs):
        self.clear_page()
        self.current_page = page_class(self.content, *args, **kwargs)
        self.current_page.grid(row=0, column=0, sticky="nsew")
        self.set_status(status_message)

    def open_section(self, key):
        config = self.page_config[key]
        page_class = config["page"]

        if page_class is PlaceholderPage:
            self.show_page(page_class, config["status"], config["title"])
            return

        self.show_page(page_class, config["status"])

    def show_dashboard(self):
        self.open_section("dashboard")

    def show_products(self):
        self.open_section("products")

    def show_customers(self):
        self.open_section("customers")

    def show_suppliers(self):
        self.open_section("suppliers")

    def show_categories(self):
        self.open_section("categories")

    def show_inventory(self):
        self.open_section("inventory")

    def show_orders(self):
        self.open_section("orders")

    def show_orderitems(self):
        self.open_section("orderitems")

    def show_payments(self):
        self.open_section("payments")

    def show_reports(self):
        self.open_section("reports")


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
