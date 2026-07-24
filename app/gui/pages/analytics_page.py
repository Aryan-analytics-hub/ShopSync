"""Filter-driven business analytics for the ShopSync desktop application."""

import csv
import html
import tkinter as tk
import textwrap
from datetime import datetime
from tkinter import filedialog, messagebox, ttk

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from database import get_connection
from gui.widgets.table_style import setup_table_style


class AnalyticsPage(ctk.CTkFrame):
    """A BI-style view of sales, inventory, product, customer and payment data."""

    BG = "#1F2937"
    BORDER = "#334155"
    TEXT = "#CBD5E1"
    PALETTE = ("#3B82F6", "#10B981", "#8B5CF6", "#F59E0B", "#06B6D4", "#F97316")

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.summary_var = tk.StringVar(value="Loading business analytics…")
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()
        self.category_var = tk.StringVar(value="All Categories")
        self.supplier_var = tk.StringVar(value="All Suppliers")
        self.customer_var = tk.StringVar(value="All Customers")
        self.payment_var = tk.StringVar(value="All Statuses")
        self.export_rows = []
        self.recommendation_rows = []
        self.analytics_tables = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.grid(row=0, column=0, sticky="nsew")
        self.scroll.grid_columnconfigure(0, weight=1)
        self.scroll.grid_columnconfigure(1, weight=1)
        self._build_header()
        self._build_tabs()
        self._load_filter_values()
        self.refresh_analytics()

    def _build_header(self):
        header = ctk.CTkFrame(self.scroll, fg_color=self.BG, corner_radius=20, border_width=1, border_color=self.BORDER)
        header.grid(row=0, column=0, columnspan=2, padx=24, pady=(24, 16), sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text="Data Analytics", font=("Segoe UI", 30, "bold"), text_color="white").grid(row=0, column=0, padx=24, pady=(20, 3), sticky="w")
        ctk.CTkLabel(header, textvariable=self.summary_var, font=("Segoe UI", 13), text_color=self.TEXT).grid(row=1, column=0, padx=24, pady=(0, 16), sticky="w")

        filters = ctk.CTkFrame(header, fg_color="#111827", corner_radius=14)
        filters.grid(row=2, column=0, padx=18, pady=(0, 18), sticky="ew")
        for col in range(7):
            filters.grid_columnconfigure(col, weight=1 if col < 5 else 0)
        self._filter_entry(filters, "From (YYYY-MM-DD)", self.start_date_var, 0)
        self._filter_entry(filters, "To (YYYY-MM-DD)", self.end_date_var, 1)
        self._filter_combo(filters, "Category", self.category_var, 2)
        self._filter_combo(filters, "Supplier", self.supplier_var, 3)
        self._filter_combo(filters, "Customer", self.customer_var, 4)
        self._filter_combo(filters, "Payment status", self.payment_var, 5)
        actions = ctk.CTkFrame(filters, fg_color="transparent")
        actions.grid(row=0, column=6, padx=(6, 12), pady=10, sticky="sew")
        ctk.CTkButton(actions, text="Apply", width=76, height=34, command=self.refresh_analytics).pack(side="left", padx=3)
        ctk.CTkButton(actions, text="CSV", width=58, height=34, fg_color="#334155", hover_color="#475569", command=self.export_csv).pack(side="left", padx=3)
        ctk.CTkButton(actions, text="Excel", width=62, height=34, fg_color="#0F766E", hover_color="#115E59", command=self.export_excel).pack(side="left", padx=3)

    def _build_tabs(self):
        """Keep the existing header intact and render one analytics area at a time."""
        self.tabview = ctk.CTkTabview(
            self.scroll,
            fg_color="transparent",
            segmented_button_fg_color="#1F2937",
            segmented_button_selected_color="#2563EB",
            segmented_button_selected_hover_color="#1D4ED8",
            segmented_button_unselected_color="#334155",
            segmented_button_unselected_hover_color="#475569",
            command=self._on_tab_changed,
        )
        self.tabview.grid(row=1, column=0, columnspan=2, padx=24, pady=(0, 24), sticky="nsew")
        self._tabs = ("Sales", "Inventory", "Products", "Customers", "Suppliers", "Payments", "Insights")
        for name in self._tabs:
            page = self.tabview.add(name)
            page.configure(fg_color="transparent")
            page.grid_columnconfigure(0, weight=1)
            page.grid_columnconfigure(1, weight=1)
        self._content_parent = self.tabview.tab("Sales")

    def _on_tab_changed(self):
        self.refresh_analytics()

    def _filter_entry(self, parent, label, variable, column):
        box = ctk.CTkFrame(parent, fg_color="transparent")
        box.grid(row=0, column=column, padx=(12, 4), pady=8, sticky="ew")
        ctk.CTkLabel(box, text=label, font=("Segoe UI", 11, "bold"), text_color=self.TEXT).pack(anchor="w")
        entry = ctk.CTkEntry(box, textvariable=variable, height=34, placeholder_text="All time")
        entry.pack(fill="x", pady=(3, 0))
        entry.bind("<Return>", lambda _event: self.refresh_analytics())

    def _filter_combo(self, parent, label, variable, column):
        box = ctk.CTkFrame(parent, fg_color="transparent")
        box.grid(row=0, column=column, padx=4, pady=8, sticky="ew")
        ctk.CTkLabel(box, text=label, font=("Segoe UI", 11, "bold"), text_color=self.TEXT).pack(anchor="w")
        combo = ctk.CTkComboBox(box, variable=variable, height=34, state="readonly", command=lambda _value: self.refresh_analytics())
        combo.pack(fill="x", pady=(3, 0))
        setattr(self, f"{label.lower().replace(' ', '_').replace('-', '_')}_combo", combo)

    def _query(self, sql, params=()):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def _load_filter_values(self):
        try:
            categories = ["All Categories"] + [str(row[0]) for row in self._query("SELECT CategoryName FROM Categories ORDER BY CategoryName")]
            suppliers = ["All Suppliers"] + [str(row[0]) for row in self._query("SELECT SupplierName FROM Suppliers ORDER BY SupplierName")]
            customers = ["All Customers"] + [f"{row.FirstName} {row.LastName or ''}".strip() for row in self._query("SELECT FirstName, LastName FROM Customers ORDER BY FirstName, LastName")]
            statuses = ["All Statuses"] + [str(row[0]) for row in self._query("SELECT DISTINCT PaymentStatus FROM Payments WHERE PaymentStatus IS NOT NULL ORDER BY PaymentStatus")]
            self.category_combo.configure(values=categories)
            self.supplier_combo.configure(values=suppliers)
            self.customer_combo.configure(values=customers)
            self.payment_status_combo.configure(values=statuses)
        except Exception as error:
            self.summary_var.set(f"Unable to load analytics filters: {error}")

    def _filters(self):
        """Return reusable WHERE clauses for order, payment and inventory queries."""
        clauses, params = [], []
        for value, label, operator in ((self.start_date_var.get().strip(), "start", ">="), (self.end_date_var.get().strip(), "end", "<")):
            if value:
                try:
                    date_value = datetime.strptime(value, "%Y-%m-%d")
                except ValueError as error:
                    raise ValueError("Dates must use YYYY-MM-DD.") from error
                if label == "end":
                    clauses.append("O.OrderDate < DATEADD(day, 1, ?)")
                else:
                    clauses.append("O.OrderDate >= ?")
                params.append(date_value)
        if self.category_var.get() != "All Categories":
            clauses.append("C.CategoryName = ?"); params.append(self.category_var.get())
        if self.supplier_var.get() != "All Suppliers":
            clauses.append("S.SupplierName = ?"); params.append(self.supplier_var.get())
        if self.customer_var.get() != "All Customers":
            clauses.append("CONCAT(CU.FirstName, ' ', ISNULL(CU.LastName, '')) = ?"); params.append(self.customer_var.get())
        if self.payment_var.get() != "All Statuses":
            clauses.append("EXISTS (SELECT 1 FROM Payments FP WHERE FP.OrderID = O.OrderID AND FP.PaymentStatus = ?)"); params.append(self.payment_var.get())
        return (" AND " + " AND ".join(clauses) if clauses else ""), tuple(params)

    def _base(self, select, group="", order="", top=""):
        where, params = self._filters()
        sql = f"""SELECT {top} {select}
            FROM Orders O
            INNER JOIN OrderItems OI ON OI.OrderID = O.OrderID
            INNER JOIN Products P ON P.ProductID = OI.ProductID
            LEFT JOIN Categories C ON C.CategoryID = P.CategoryID
            LEFT JOIN Suppliers S ON S.SupplierID = P.SupplierID
            LEFT JOIN Customers CU ON CU.CustomerID = O.CustomerID
            WHERE 1 = 1 {where} {group} {order}"""
        return self._query(sql, params)

    def _section(self, title, subtitle, row):
        frame = ctk.CTkFrame(self._content_parent, fg_color="transparent")
        frame.grid(row=row, column=0, columnspan=2, padx=24, pady=(18, 5), sticky="ew")
        ctk.CTkLabel(frame, text=title, font=("Segoe UI", 22, "bold"), text_color="white").pack(anchor="w")
        ctk.CTkLabel(frame, text=subtitle, font=("Segoe UI", 12), text_color="#94A3B8").pack(anchor="w", pady=(0, 6))
        return row + 1

    def _chart_card(self, title, row, column, columns=2):
        card = ctk.CTkFrame(self._content_parent, fg_color=self.BG, corner_radius=16, border_width=1, border_color=self.BORDER)
        card.grid(row=row, column=column, columnspan=1, padx=(0, 8) if column == 0 else (8, 0), pady=(0, 14), sticky="nsew")
        ctk.CTkLabel(card, text=title, font=("Segoe UI", 15, "bold"), text_color="white").pack(anchor="w", padx=16, pady=(13, 2))
        figure = Figure(figsize=(6.35, 3.55), dpi=100, facecolor=self.BG, constrained_layout=True)
        axis = figure.add_subplot(111)
        canvas = FigureCanvasTkAgg(figure, master=card)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 10))
        return axis, canvas

    def _charts_row(self, row):
        self._content_parent.grid_columnconfigure(0, weight=1)
        self._content_parent.grid_columnconfigure(1, weight=1)
        return row

    def _style_axis(self, axis):
        axis.set_facecolor(self.BG)
        axis.tick_params(colors=self.TEXT, labelsize=8, pad=6)
        for spine in axis.spines.values(): spine.set_color("#475569")
        axis.grid(axis="y", color="#475569", alpha=.35, linewidth=.7)
        axis.set_axisbelow(True)
        axis.margins(x=.03, y=.14)

    def _plot(self, title, labels, values, row, column, kind="bar", color=None):
        axis, canvas = self._chart_card(title, row, column)
        self._style_axis(axis)
        color = color or self.PALETTE[column]
        if not values:
            axis.text(.5, .5, "No data for current filters", ha="center", va="center", color="#94A3B8", transform=axis.transAxes)
            axis.set_xticks([]); axis.set_yticks([])
        elif kind == "line":
            axis.plot(labels, values, color=color, marker="o", markersize=4, linewidth=2.4, label=title)
            axis.fill_between(range(len(values)), values, color=color, alpha=.08)
            axis.tick_params(axis="x", rotation=28)
        elif kind == "area":
            axis.plot(labels, values, color=color, linewidth=2.4, label=title)
            axis.fill_between(range(len(values)), values, color=color, alpha=.22)
            axis.tick_params(axis="x", rotation=28)
        elif kind == "horizontal":
            axis.barh([self._short_label(label, 25) for label in labels], values, color=color, height=.64); axis.invert_yaxis()
        elif kind in ("pie", "donut"):
            pie_labels = [self._short_label(label, 18) for label in labels]
            wedges, _, _ = axis.pie(values, labels=pie_labels, colors=[self.PALETTE[i % len(self.PALETTE)] for i in range(len(values))], autopct="%1.0f%%", pctdistance=.75, labeldistance=1.06, textprops={"color": self.TEXT, "fontsize": 8})
            if kind == "donut": axis.add_artist(plt_circle(axis))
        else:
            axis.bar([self._short_label(label, 16) for label in labels], values, color=color, width=.62); axis.tick_params(axis="x", rotation=28)
        axis.yaxis.set_major_formatter(self._number_formatter(values))
        canvas.draw()

    @staticmethod
    def _short_label(value, width=20):
        return textwrap.shorten(str(value or "Uncategorised"), width=width, placeholder="…")

    @staticmethod
    def _compact_currency(value):
        value = float(value or 0)
        absolute = abs(value)
        if absolute >= 10000000:
            return f"₹{value / 10000000:.2f} Cr"
        if absolute >= 100000:
            return f"₹{value / 100000:.2f} L"
        if absolute >= 1000:
            return f"₹{value / 1000:.1f} K"
        return f"₹{value:,.2f}"

    @staticmethod
    def _number_formatter(values):
        from matplotlib.ticker import FuncFormatter
        maximum = max((abs(float(value or 0)) for value in values), default=0)
        if maximum >= 100000:
            return FuncFormatter(lambda value, _pos: f"₹{value / 100000:.1f}L")
        if maximum >= 1000:
            return FuncFormatter(lambda value, _pos: f"{value / 1000:.0f}K")
        return FuncFormatter(lambda value, _pos: f"{value:g}")

    def _table(self, title, headings, rows, row_number):
        card = ctk.CTkFrame(self._content_parent, fg_color=self.BG, corner_radius=16, border_width=1, border_color=self.BORDER)
        card.grid(row=row_number, column=0, columnspan=2, padx=0, pady=(0, 14), sticky="ew")
        ctk.CTkLabel(card, text=title, font=("Segoe UI", 15, "bold"), text_color="white").pack(anchor="w", padx=16, pady=(13, 6))
        setup_table_style()
        tree = ttk.Treeview(card, columns=tuple(range(len(headings))), show="headings", height=min(max(len(rows), 3), 7))
        for index, heading in enumerate(headings):
            tree.heading(index, text=heading); tree.column(index, anchor="w", width=max(120, 820 // len(headings)), stretch=True)
        for index, row in enumerate(rows):
            tree.insert("", "end", values=tuple(row), tags=("even" if index % 2 == 0 else "odd",))
        tree.tag_configure("even", background="#162032", foreground="#E2E8F0")
        tree.tag_configure("odd", background="#111827", foreground="#CBD5E1")
        style = ttk.Style()
        style.configure("Treeview", rowheight=29, font=("Segoe UI", 10))
        tree.pack(fill="x", padx=14, pady=(0, 14))
        self.analytics_tables.append((title, headings, [tuple(item) for item in rows]))

    def refresh_analytics(self):
        try:
            self._filters()  # validate before clearing the current view
            self.analytics_tables = []
            self.export_rows = []
            self.recommendation_rows = []
            active_tab = self.tabview.get()
            self._content_parent = self.tabview.tab(active_tab)
            for widget in self._content_parent.winfo_children():
                widget.destroy()
            renderers = {
                "Sales": self._sales,
                "Inventory": self._inventory,
                "Products": self._products,
                "Customers": self._customers,
                "Suppliers": self._suppliers,
                "Payments": self._payments,
                "Insights": self._render_insights_tab,
            }
            renderers[active_tab](0)
            self.summary_var.set(f"{active_tab} analytics reflect the current database filters")
        except Exception as error:
            self.summary_var.set(f"Unable to refresh analytics: {error}")

    def _render_insights_tab(self, row):
        row = self._insights(row)
        self._recommendations(row)

    def _sales(self, row):
        row = self._section("Sales Analytics", "Sales movement, order demand and category mix", row)
        monthly = self._base("CONVERT(char(7), O.OrderDate, 120) Month, SUM(OI.Quantity * OI.UnitPrice) Revenue, COUNT(DISTINCT O.OrderID) Orders", "GROUP BY CONVERT(char(7), O.OrderDate, 120)", "ORDER BY Month")
        top = self._base("TOP 10 P.ProductName, SUM(OI.Quantity) Units", "GROUP BY P.ProductName", "ORDER BY Units DESC")
        bottom = self._base("TOP 10 P.ProductName, SUM(OI.Quantity) Units", "GROUP BY P.ProductName", "ORDER BY Units ASC")
        categories = self._base("C.CategoryName, SUM(OI.Quantity * OI.UnitPrice) Revenue", "GROUP BY C.CategoryName", "ORDER BY Revenue DESC")
        self._plot("Monthly Sales Trend", [r.Month for r in monthly], [float(r.Revenue or 0) for r in monthly], row, 0, "line", "#10B981")
        self._plot("Monthly Orders", [r.Month for r in monthly], [r.Orders for r in monthly], row, 1, "bar", "#3B82F6"); row += 1
        self._plot("Top 10 Selling Products", [r.ProductName for r in top], [r.Units for r in top], row, 0, "horizontal", "#F59E0B")
        self._plot("Revenue Trend", [r.Month for r in monthly], [float(r.Revenue or 0) for r in monthly], row, 1, "area", "#06B6D4"); row += 1
        self._table("Bottom 10 Selling Products · Sales by Category", ("Product", "Units Sold"), [(r.ProductName, r.Units) for r in bottom], row); row += 1
        self._table("Category Revenue", ("Category", "Revenue"), [(r.CategoryName or "Uncategorised", self._compact_currency(r.Revenue)) for r in categories], row); return row + 1

    def _inventory(self, row):
        row = self._section("Inventory Analytics", "Stock balance, value exposure and replenishment priorities", row)
        where, params = self._filters()
        # Inventory respects product filters directly; date/customer/payment filters limit it to products sold in matching orders.
        product_filter = "" if not where else f" WHERE EXISTS (SELECT 1 FROM Orders O INNER JOIN OrderItems OI ON OI.OrderID=O.OrderID INNER JOIN Customers CU ON CU.CustomerID=O.CustomerID WHERE OI.ProductID=P.ProductID {where})"
        inventory = self._query(f"SELECT C.CategoryName, SUM(ISNULL(I.Quantity,0)) Quantity, SUM(ISNULL(I.Quantity,0)*P.CostPrice) Value FROM Products P LEFT JOIN Inventory I ON I.ProductID=P.ProductID LEFT JOIN Categories C ON C.CategoryID=P.CategoryID LEFT JOIN Suppliers S ON S.SupplierID=P.SupplierID {product_filter} GROUP BY C.CategoryName ORDER BY Quantity DESC", params)
        movement = self._base("P.ProductName, SUM(OI.Quantity) Units", "GROUP BY P.ProductName", "ORDER BY Units DESC")
        stock = self._query(f"SELECT P.ProductName, ISNULL(I.Quantity,0) Quantity, ISNULL(I.ReorderLevel,0) ReorderLevel, ISNULL(M.Units,0) UnitsSold FROM Products P LEFT JOIN Inventory I ON I.ProductID=P.ProductID LEFT JOIN (SELECT OI.ProductID, SUM(OI.Quantity) Units FROM Orders O INNER JOIN OrderItems OI ON OI.OrderID=O.OrderID INNER JOIN Products FP ON FP.ProductID=OI.ProductID LEFT JOIN Categories C ON C.CategoryID=FP.CategoryID LEFT JOIN Suppliers S ON S.SupplierID=FP.SupplierID LEFT JOIN Customers CU ON CU.CustomerID=O.CustomerID WHERE 1=1 {where} GROUP BY OI.ProductID) M ON M.ProductID=P.ProductID LEFT JOIN Categories C ON C.CategoryID=P.CategoryID LEFT JOIN Suppliers S ON S.SupplierID=P.SupplierID {product_filter} ORDER BY UnitsSold DESC", params + params)
        self._plot("Inventory Distribution by Category", [r.CategoryName or "Uncategorised" for r in inventory], [float(r.Quantity or 0) for r in inventory], row, 0, "donut")
        self._plot("Inventory Value by Category", [r.CategoryName or "Uncategorised" for r in inventory], [float(r.Value or 0) for r in inventory], row, 1, "bar", "#8B5CF6"); row += 1
        self._plot("Fast Moving Products", [r.ProductName for r in movement[:10]], [r.Units for r in movement[:10]], row, 0, "horizontal", "#10B981")
        slow = list(reversed(movement[-10:]))
        self._plot("Slow Moving Products", [r.ProductName for r in slow], [r.Units for r in slow], row, 1, "horizontal", "#F97316"); row += 1
        exceptions = [(r.ProductName, r.Quantity, r.ReorderLevel, r.UnitsSold, "LOW STOCK" if r.Quantity <= r.ReorderLevel else "DEAD STOCK" if r.UnitsSold == 0 and r.Quantity > 0 else "In stock") for r in stock if r.Quantity <= r.ReorderLevel or (r.UnitsSold == 0 and r.Quantity > 0)]
        self._table("Low Stock and Dead Stock Products", ("Product", "On hand", "Reorder", "Units sold", "Action"), exceptions[:25], row); return row + 1

    def _products(self, row):
        row = self._section("Product Analytics", "Product contribution and category performance comparison", row)
        products = self._base("P.ProductName, C.CategoryName, SUM(OI.Quantity) Units, SUM(OI.Quantity*OI.UnitPrice) Revenue", "GROUP BY P.ProductName, C.CategoryName", "ORDER BY Revenue DESC")
        cats = self._base("C.CategoryName, SUM(OI.Quantity*OI.UnitPrice) Revenue", "GROUP BY C.CategoryName", "ORDER BY Revenue DESC")
        self._plot("Best Performing Products", [r.ProductName for r in products[:10]], [float(r.Revenue) for r in products[:10]], row, 0, "horizontal", "#10B981")
        self._plot("Product Performance by Category", [r.CategoryName or "Uncategorised" for r in cats], [float(r.Revenue) for r in cats], row, 1, "bar", "#8B5CF6"); row += 1
        self._table("Worst Performing Products", ("Product", "Category", "Units", "Revenue"), [(r.ProductName, r.CategoryName or "Uncategorised", r.Units, self._compact_currency(r.Revenue)) for r in products[-10:]], row); row += 1
        self._table("Product Sales Comparison", ("Product", "Category", "Units sold", "Revenue"), [(r.ProductName, r.CategoryName or "Uncategorised", r.Units, self._compact_currency(r.Revenue)) for r in products[:15]], row); return row + 1

    def _customers(self, row):
        row = self._section("Customer Analytics", "Who buys most, how often they buy and their spend profile", row)
        where, params = self._filters()
        customers = self._query(f"SELECT CONCAT(CU.FirstName, ' ', ISNULL(CU.LastName,'')) Customer, COUNT(DISTINCT O.OrderID) Orders, SUM(OI.Quantity*OI.UnitPrice) Spend FROM Orders O INNER JOIN OrderItems OI ON OI.OrderID=O.OrderID INNER JOIN Products P ON P.ProductID=OI.ProductID LEFT JOIN Categories C ON C.CategoryID=P.CategoryID LEFT JOIN Suppliers S ON S.SupplierID=P.SupplierID INNER JOIN Customers CU ON CU.CustomerID=O.CustomerID WHERE 1=1 {where} GROUP BY CU.FirstName, CU.LastName ORDER BY Spend DESC", params)
        frequency = [("Repeat (2+ orders)", sum(1 for r in customers if r.Orders >= 2)), ("New / one order", sum(1 for r in customers if r.Orders < 2))]
        self._plot("Top Customers", [r.Customer for r in customers[:10]], [float(r.Spend) for r in customers[:10]], row, 0, "horizontal", "#3B82F6")
        self._plot("Repeat Customers vs New Customers", [x[0] for x in frequency], [x[1] for x in frequency], row, 1, "donut"); row += 1
        spend_bands = [("< 5k", sum(1 for r in customers if float(r.Spend) < 5000)), ("5k–20k", sum(1 for r in customers if 5000 <= float(r.Spend) < 20000)), ("20k+", sum(1 for r in customers if float(r.Spend) >= 20000))]
        self._plot("Customer Spending Distribution", [x[0] for x in spend_bands], [x[1] for x in spend_bands], row, 0, "bar", "#F59E0B")
        self._table("Customer Purchase Frequency", ("Customer", "Orders", "Total spend"), [(r.Customer, r.Orders, self._compact_currency(r.Spend)) for r in customers[:20]], row); return row + 1

    def _suppliers(self, row):
        row = self._section("Supplier Analytics", "Supplier coverage, inventory contribution and product concentration", row)
        where, params = self._filters()
        supplier_filter = "" if not where else f" WHERE EXISTS (SELECT 1 FROM Orders O INNER JOIN OrderItems OI ON OI.OrderID=O.OrderID INNER JOIN Customers CU ON CU.CustomerID=O.CustomerID INNER JOIN Products FP ON FP.ProductID=OI.ProductID LEFT JOIN Categories C ON C.CategoryID=FP.CategoryID LEFT JOIN Suppliers FS ON FS.SupplierID=FP.SupplierID WHERE FP.SupplierID=P.SupplierID {where})"
        suppliers = self._query(f"SELECT S.SupplierName, COUNT(P.ProductID) Products, SUM(ISNULL(I.Quantity,0)) Inventory, SUM(ISNULL(I.Quantity,0)*P.CostPrice) Value FROM Suppliers S LEFT JOIN Products P ON P.SupplierID=S.SupplierID LEFT JOIN Inventory I ON I.ProductID=P.ProductID LEFT JOIN Categories C ON C.CategoryID=P.CategoryID {supplier_filter} GROUP BY S.SupplierName ORDER BY Inventory DESC", params)
        self._plot("Supplier-wise Inventory", [r.SupplierName for r in suppliers[:10]], [float(r.Inventory or 0) for r in suppliers[:10]], row, 0, "horizontal", "#06B6D4")
        self._plot("Products per Supplier", [r.SupplierName for r in suppliers[:10]], [r.Products for r in suppliers[:10]], row, 1, "bar", "#8B5CF6"); row += 1
        self._table("Supplier Contribution and Ranking", ("Rank", "Supplier", "Products", "Inventory", "Inventory value"), [(index + 1, r.SupplierName, r.Products, r.Inventory or 0, self._compact_currency(r.Value)) for index, r in enumerate(suppliers[:20])], row); return row + 1

    def _payments(self, row):
        row = self._section("Payment Analytics", "Collection timing, settlement status and refunds", row)
        where, params = self._filters()
        # Select each payment once before aggregating because an order can contain many items.
        filtered_payments = f"""SELECT DISTINCT PAY.PaymentID, PAY.PaymentDate, PAY.PaymentStatus, PAY.Amount
            FROM Payments PAY
            INNER JOIN Orders O ON O.OrderID = PAY.OrderID
            INNER JOIN OrderItems OI ON OI.OrderID = O.OrderID
            INNER JOIN Products P ON P.ProductID = OI.ProductID
            LEFT JOIN Categories C ON C.CategoryID = P.CategoryID
            LEFT JOIN Suppliers S ON S.SupplierID = P.SupplierID
            LEFT JOIN Customers CU ON CU.CustomerID = O.CustomerID
            WHERE 1 = 1 {where}"""
        payments = self._query(f"SELECT PaymentStatus, COUNT(*) PaymentCount, SUM(Amount) Amount FROM ({filtered_payments}) FP GROUP BY PaymentStatus", params)
        collection = self._query(f"SELECT CONVERT(char(7), PaymentDate, 120) Month, SUM(Amount) Amount FROM ({filtered_payments}) FP WHERE PaymentStatus = 'Completed' GROUP BY CONVERT(char(7), PaymentDate, 120) ORDER BY Month", params)
        self._plot("Payment Status Distribution", [r.PaymentStatus for r in payments], [r.PaymentCount for r in payments], row, 0, "donut")
        self._plot("Monthly Payment Collection", [r.Month for r in collection], [float(r.Amount or 0) for r in collection], row, 1, "area", "#10B981"); row += 1
        self._table("Pending vs Completed Payments · Refund Analysis", ("Status", "Payments", "Amount"), [(r.PaymentStatus, r.PaymentCount, self._compact_currency(r.Amount)) for r in payments], row); return row + 1

    def _insights(self, row):
        row = self._section("Business Insights", "Automatically calculated from current filters — no AI-generated conclusions", row)
        products = self._base("P.ProductName, SUM(OI.Quantity) Units, SUM(OI.Quantity*OI.UnitPrice) Revenue", "GROUP BY P.ProductName", "ORDER BY Units DESC")
        categories = self._base("C.CategoryName, SUM(OI.Quantity*OI.UnitPrice) Revenue", "GROUP BY C.CategoryName", "ORDER BY Revenue DESC")
        category_units = self._base("C.CategoryName, SUM(OI.Quantity) Units", "GROUP BY C.CategoryName", "ORDER BY Units DESC")
        profitable_categories = self._base("C.CategoryName, SUM(OI.Quantity * (OI.UnitPrice - P.CostPrice)) Profit", "GROUP BY C.CategoryName", "ORDER BY Profit DESC")
        monthly = self._base("CONVERT(char(7), O.OrderDate, 120) Month, SUM(OI.Quantity*OI.UnitPrice) Revenue, COUNT(DISTINCT O.OrderID) Orders", "GROUP BY CONVERT(char(7), O.OrderDate, 120)", "ORDER BY Month")
        customers = self._base("CONCAT(CU.FirstName, ' ', ISNULL(CU.LastName, '')) Customer, SUM(OI.Quantity*OI.UnitPrice) Spend", "GROUP BY CU.FirstName, CU.LastName", "ORDER BY Spend DESC")
        where, params = self._filters()
        stock_scope = "" if not where else f" AND EXISTS (SELECT 1 FROM Orders O INNER JOIN OrderItems OI ON OI.OrderID=O.OrderID INNER JOIN Customers CU ON CU.CustomerID=O.CustomerID WHERE OI.ProductID=P.ProductID {where})"
        stock = self._query(f"SELECT P.ProductName, I.Quantity, I.ReorderLevel FROM Products P INNER JOIN Inventory I ON I.ProductID=P.ProductID LEFT JOIN Categories C ON C.CategoryID=P.CategoryID LEFT JOIN Suppliers S ON S.SupplierID=P.SupplierID WHERE I.Quantity <= I.ReorderLevel {stock_scope}", params)
        totals = self._query("SELECT ISNULL(SUM(I.Quantity*P.CostPrice),0) Value FROM Products P LEFT JOIN Inventory I ON I.ProductID=P.ProductID")[0]
        inventory_units = self._query("SELECT ISNULL(SUM(Quantity), 0) Quantity FROM Inventory")[0]
        out_of_stock = self._query("SELECT COUNT(*) Total FROM Inventory WHERE ISNULL(Quantity, 0) = 0")[0]
        never_sold = self._query("SELECT COUNT(*) Total FROM Products P WHERE NOT EXISTS (SELECT 1 FROM OrderItems OI WHERE OI.ProductID = P.ProductID)")[0]
        filtered_orders = f"""SELECT DISTINCT O.OrderID, O.TotalAmount, O.OrderStatus
            FROM Orders O
            INNER JOIN OrderItems OI ON OI.OrderID = O.OrderID
            INNER JOIN Products P ON P.ProductID = OI.ProductID
            LEFT JOIN Categories C ON C.CategoryID = P.CategoryID
            LEFT JOIN Suppliers S ON S.SupplierID = P.SupplierID
            LEFT JOIN Customers CU ON CU.CustomerID = O.CustomerID
            WHERE 1 = 1 {where}"""
        order_totals = self._query(f"SELECT COUNT(*) Orders, AVG(CAST(TotalAmount AS float)) AverageOrder FROM ({filtered_orders}) FO", params)
        supplier = self._query("SELECT TOP 1 S.SupplierName FROM Suppliers S INNER JOIN Products P ON P.SupplierID=S.SupplierID LEFT JOIN Inventory I ON I.ProductID=P.ProductID GROUP BY S.SupplierName ORDER BY SUM(ISNULL(I.Quantity,0)) DESC")
        pending = self._query(f"SELECT CAST(100.0 * SUM(CASE WHEN OrderStatus = 'Pending' THEN 1 ELSE 0 END) / NULLIF(COUNT(*),0) AS decimal(10,1)) Rate FROM ({filtered_orders}) FO", params)[0]
        insights = [
            ("Highest selling product", products[0].ProductName if products else "No sales data"),
            ("Lowest selling product", products[-1].ProductName if products else "No sales data"),
            ("Highest revenue category", categories[0].CategoryName if categories else "No sales data"),
            ("Lowest revenue category", categories[-1].CategoryName if categories else "No sales data"),
            ("Products needing immediate reorder", ", ".join(r.ProductName for r in stock[:5]) or "None"),
            ("Supplier contributing the most inventory", supplier[0].SupplierName if supplier else "No supplier data"),
            ("Total inventory value", self._compact_currency(totals.Value)),
            ("Average order value", self._compact_currency(order_totals[0].AverageOrder) if order_totals else self._compact_currency(0)),
            ("Pending order percentage", f"{float(pending.Rate or 0):.1f}%"),
            ("Average monthly revenue", self._compact_currency(sum(float(r.Revenue or 0) for r in monthly) / len(monthly)) if monthly else self._compact_currency(0)),
            ("Average monthly orders", f"{sum(float(r.Orders or 0) for r in monthly) / len(monthly):.1f}" if monthly else "0"),
            ("Inventory turnover estimate", f"{sum(float(r.Units or 0) for r in products) / max(float(inventory_units.Quantity or 0), 1):.2f}x"),
            ("Products never sold", str(never_sold.Total or 0)),
            ("Products out of stock", str(out_of_stock.Total or 0)),
            ("Highest value customer", customers[0].Customer if customers else "No customer data"),
            ("Fastest moving category", category_units[0].CategoryName if category_units else "No category data"),
            ("Slowest moving category", category_units[-1].CategoryName if category_units else "No category data"),
            ("Most profitable category", profitable_categories[0].CategoryName if profitable_categories else "No category data"),
            ("Most ordered category", category_units[0].CategoryName if category_units else "No category data"),
            ("Estimated reorder priority", f"{len(stock)} product(s) at or below reorder level"),
        ]
        self._table("Business Insights", ("Insight", "Current result"), insights, row)
        self.export_rows = insights
        return row + 1

    def _recommendations(self, row):
        row = self._section("Business Recommendations", "Rule-based actions generated from the filtered operational data", row)
        where, params = self._filters()
        scope = "" if not where else f" AND EXISTS (SELECT 1 FROM Orders O INNER JOIN OrderItems OI ON OI.OrderID=O.OrderID INNER JOIN Customers CU ON CU.CustomerID=O.CustomerID WHERE OI.ProductID=P.ProductID {where})"
        low_stock = self._query(f"""SELECT TOP 5 P.ProductName, I.Quantity, I.ReorderLevel
            FROM Inventory I INNER JOIN Products P ON P.ProductID=I.ProductID
            LEFT JOIN Categories C ON C.CategoryID=P.CategoryID LEFT JOIN Suppliers S ON S.SupplierID=P.SupplierID
            WHERE I.Quantity <= I.ReorderLevel {scope} ORDER BY I.Quantity ASC""", params)
        dead_stock = self._query(f"""SELECT TOP 3 P.ProductName, I.Quantity
            FROM Products P INNER JOIN Inventory I ON I.ProductID=P.ProductID
            LEFT JOIN Categories C ON C.CategoryID=P.CategoryID LEFT JOIN Suppliers S ON S.SupplierID=P.SupplierID
            WHERE I.Quantity > 0 AND NOT EXISTS (SELECT 1 FROM OrderItems OI WHERE OI.ProductID=P.ProductID)
            {scope} ORDER BY I.Quantity DESC""", params)
        payment_scope = f"""SELECT DISTINCT PAY.PaymentID, PAY.Amount FROM Payments PAY
            INNER JOIN Orders O ON O.OrderID=PAY.OrderID INNER JOIN OrderItems OI ON OI.OrderID=O.OrderID
            INNER JOIN Products P ON P.ProductID=OI.ProductID LEFT JOIN Categories C ON C.CategoryID=P.CategoryID
            LEFT JOIN Suppliers S ON S.SupplierID=P.SupplierID LEFT JOIN Customers CU ON CU.CustomerID=O.CustomerID
            WHERE PAY.PaymentStatus='Pending' {where}"""
        payment_pending = self._query(f"SELECT ISNULL(SUM(Amount), 0) Amount FROM ({payment_scope}) PendingPayments", params)[0]
        supplier = self._query("""SELECT TOP 1 S.SupplierName, SUM(ISNULL(I.Quantity,0)) Units
            FROM Suppliers S INNER JOIN Products P ON P.SupplierID=S.SupplierID
            LEFT JOIN Inventory I ON I.ProductID=P.ProductID GROUP BY S.SupplierName ORDER BY Units DESC""")
        total_units = self._query("SELECT ISNULL(SUM(Quantity), 0) Units FROM Inventory")[0]
        recommendations = []
        recommendations.extend(("Restock", f"Restock {item.ProductName}: {item.Quantity} on hand against a reorder level of {item.ReorderLevel}.") for item in low_stock)
        recommendations.extend(("Reduce dead stock", f"Review {item.ProductName}: {item.Quantity} units have never been sold.") for item in dead_stock)
        if supplier and total_units.Units:
            share = float(supplier[0].Units or 0) * 100 / float(total_units.Units)
            recommendations.append(("Supplier concentration", f"{supplier[0].SupplierName} contributes {share:.1f}% of current inventory; monitor concentration risk."))
        if float(payment_pending.Amount or 0) > 50000:
            recommendations.append(("Collections", f"Pending payments total {self._compact_currency(payment_pending.Amount)}; prioritise follow-up."))
        if not recommendations:
            recommendations.append(("Operational health", "No urgent stock, dead-stock or payment exceptions were found for the current data."))
        self.recommendation_rows = recommendations
        self._table("Business Recommendations", ("Focus", "Recommended action"), recommendations, row)

    def export_csv(self):
        if not self.analytics_tables: return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Export Analytics Report")
        if path:
            with open(path, "w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file)
                for title, headings, rows in self.analytics_tables:
                    writer.writerow((title,))
                    writer.writerow(headings)
                    writer.writerows(rows)
                    writer.writerow(())
            self.summary_var.set(f"Analytics report exported to {path}")

    def export_excel(self):
        if not self.analytics_tables: return
        path = filedialog.asksaveasfilename(defaultextension=".xls", filetypes=[("Excel files", "*.xls")], title="Export Analytics Report")
        if path:
            tables = []
            for title, headings, rows in self.analytics_tables:
                body = "".join("<tr>" + "".join(f"<td>{html.escape(str(value))}</td>" for value in record) + "</tr>" for record in rows)
                header = "".join(f"<th>{html.escape(str(heading))}</th>" for heading in headings)
                tables.append(f"<h2>{html.escape(title)}</h2><table><tr>{header}</tr>{body}</table>")
            with open(path, "w", encoding="utf-8") as file:
                file.write("<html><head><meta charset='utf-8'><style>body{font-family:Segoe UI;color:#172033}h1{color:#1d4ed8}h2{margin-top:24px;color:#0f766e}table{border-collapse:collapse;width:100%;margin-bottom:18px}th{background:#1f2937;color:white;text-align:left}th,td{border:1px solid #cbd5e1;padding:7px}tr:nth-child(even){background:#f1f5f9}</style></head><body><h1>ShopSync Analytics Report</h1>" + "".join(tables) + "</body></html>")
            self.summary_var.set(f"Analytics report exported to {path}")


def plt_circle(axis):
    """Create the centre of a doughnut chart without importing pyplot."""
    from matplotlib.patches import Circle
    return Circle((0, 0), 0.58, fc=AnalyticsPage.BG)
