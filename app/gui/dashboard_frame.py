from datetime import datetime
import tkinter as tk
from tkinter import ttk

import customtkinter as ctk

from database import get_connection
from gui.widgets.table_style import setup_table_style


class MetricCard(ctk.CTkFrame):
    def __init__(self, master, title, value, accent, note=""):
        super().__init__(
            master,
            fg_color="#1F2937",
            corner_radius=18,
            border_width=1,
            border_color=accent,
            height=120
        )
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 14, "bold"),
            text_color="#CBD5E1"
        ).grid(row=0, column=0, padx=18, pady=(16, 6), sticky="w")

        ctk.CTkLabel(
            self,
            text=value,
            font=("Segoe UI", 28, "bold"),
            text_color="white"
        ).grid(row=1, column=0, padx=18, sticky="w")

        ctk.CTkLabel(
            self,
            text=note,
            font=("Segoe UI", 12),
            text_color=accent
        ).grid(row=2, column=0, padx=18, pady=(6, 14), sticky="w")


class ChartCard(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(
            master,
            fg_color="#1F2937",
            corner_radius=20,
            border_width=1,
            border_color="#334155"
        )
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 18, "bold"),
            text_color="white"
        ).grid(row=0, column=0, padx=18, pady=(16, 8), sticky="w")

        self.canvas = tk.Canvas(
            self,
            bg="#0F172A",
            highlightthickness=0,
            height=260
        )
        self.canvas.grid(row=1, column=0, padx=18, pady=(0, 18), sticky="nsew")
        self.canvas.bind("<Configure>", self._on_resize)

        self.chart_kind = None
        self.chart_data = []
        self.bar_color = "#2563EB"

    def _on_resize(self, _event):
        if self.chart_kind == "line":
            self.draw_line_chart(self.chart_data)
        elif self.chart_kind == "bar":
            self.draw_bar_chart(self.chart_data, self.bar_color)

    def draw_line_chart(self, points):
        self.chart_kind = "line"
        self.chart_data = points
        self.canvas.delete("all")

        width = max(self.canvas.winfo_width(), 640)
        height = max(self.canvas.winfo_height(), 260)

        if not points:
            self.canvas.create_text(
                width / 2,
                height / 2,
                text="No data available",
                fill="#94A3B8",
                font=("Segoe UI", 14)
            )
            return

        left = 55
        right = width - 20
        top = 20
        bottom = height - 45

        values = [float(value) for _, value in points]
        max_value = max(values) if max(values) > 0 else 1
        steps = 4

        for index in range(steps + 1):
            y = bottom - ((bottom - top) / steps) * index
            value = max_value / steps * index
            self.canvas.create_line(left, y, right, y, fill="#1E293B", width=1)
            self.canvas.create_text(
                left - 10,
                y,
                text=f"{value:.0f}",
                fill="#94A3B8",
                font=("Segoe UI", 10),
                anchor="e"
            )

        x_gap = (right - left) / max(len(points) - 1, 1)
        coordinates = []

        for index, (label, value) in enumerate(points):
            x = left + index * x_gap
            y = bottom - ((float(value) / max_value) * (bottom - top))
            coordinates.extend((x, y))
            self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill="#38BDF8", outline="")
            self.canvas.create_text(
                x,
                bottom + 16,
                text=label,
                fill="#CBD5E1",
                font=("Segoe UI", 10)
            )
            self.canvas.create_text(
                x,
                y - 14,
                text=f"{float(value):.0f}",
                fill="#E2E8F0",
                font=("Segoe UI", 9)
            )

        if len(coordinates) >= 4:
            self.canvas.create_line(*coordinates, fill="#38BDF8", width=3, smooth=True)

    def draw_bar_chart(self, items, color="#2563EB"):
        self.chart_kind = "bar"
        self.chart_data = items
        self.bar_color = color
        self.canvas.delete("all")

        width = max(self.canvas.winfo_width(), 360)
        height = max(self.canvas.winfo_height(), 260)

        if not items:
            self.canvas.create_text(
                width / 2,
                height / 2,
                text="No data available",
                fill="#94A3B8",
                font=("Segoe UI", 14)
            )
            return

        left = 18
        right = width - 18
        top = 20
        row_height = max((height - top - 12) / len(items), 34)
        max_value = max(float(value) for _, value in items) or 1

        for index, (label, value) in enumerate(items):
            y = top + index * row_height
            bar_left = left + 105
            bar_right = right - 40
            available_width = bar_right - bar_left
            bar_width = (float(value) / max_value) * available_width

            self.canvas.create_text(
                left,
                y + 12,
                text=label,
                fill="#CBD5E1",
                font=("Segoe UI", 10),
                anchor="w"
            )
            self.canvas.create_rectangle(
                bar_left,
                y + 2,
                bar_right,
                y + 22,
                fill="#1E293B",
                outline=""
            )
            self.canvas.create_rectangle(
                bar_left,
                y + 2,
                bar_left + bar_width,
                y + 22,
                fill=color,
                outline=""
            )
            self.canvas.create_text(
                right - 5,
                y + 12,
                text=str(value),
                fill="white",
                font=("Segoe UI", 10, "bold"),
                anchor="e"
            )


class TableCard(ctk.CTkFrame):
    def __init__(self, master, title, columns, headings):
        super().__init__(
            master,
            fg_color="#1F2937",
            corner_radius=20,
            border_width=1,
            border_color="#334155"
        )
        self.columns = columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 18, "bold"),
            text_color="white"
        ).grid(row=0, column=0, padx=18, pady=(16, 10), sticky="w")

        setup_table_style()

        table_frame = tk.Frame(self, bg="#1F2937", highlightthickness=0)
        table_frame.grid(row=1, column=0, padx=18, pady=(0, 18), sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)

        for column, heading, width in headings:
            self.tree.heading(column, text=heading)
            self.tree.column(column, width=width, anchor="w", stretch=True)

        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

    def populate(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in rows:
            self.tree.insert("", "end", values=row)


class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.summary_var = tk.StringVar(value="Loading dashboard...")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0
        )
        self.scroll_frame.grid(row=0, column=0, sticky="nsew")
        for column in range(4):
            self.scroll_frame.grid_columnconfigure(column, weight=1)

        self._build_header()
        self._build_metric_section()
        self._build_chart_section()
        self._build_table_section()
        self.refresh_dashboard()

    def _build_header(self):
        header = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="#1F2937",
            corner_radius=20,
            border_width=1,
            border_color="#334155"
        )
        header.grid(row=0, column=0, columnspan=4, padx=24, pady=(24, 18), sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)

        ctk.CTkLabel(
            header,
            text="Dashboard",
            font=("Segoe UI", 32, "bold"),
            text_color="white"
        ).grid(row=0, column=0, padx=24, pady=(22, 6), sticky="w")

        ctk.CTkLabel(
            header,
            textvariable=self.summary_var,
            font=("Segoe UI", 14),
            text_color="#CBD5E1"
        ).grid(row=1, column=0, padx=24, pady=(0, 20), sticky="w")

        ctk.CTkButton(
            header,
            text="Refresh Dashboard",
            width=150,
            height=40,
            corner_radius=10,
            command=self.refresh_dashboard
        ).grid(row=0, column=1, rowspan=2, padx=24, pady=20, sticky="e")

    def _build_metric_section(self):
        self.metric_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.metric_frame.grid(row=1, column=0, columnspan=4, padx=24, pady=(0, 18), sticky="ew")

        for column in range(4):
            self.metric_frame.grid_columnconfigure(column, weight=1)

    def _build_chart_section(self):
        self.sales_chart = ChartCard(self.scroll_frame, "Sales Trend (Last 7 Days)")
        self.sales_chart.grid(row=2, column=0, columnspan=2, padx=(24, 12), pady=(0, 18), sticky="nsew")

        self.order_status_chart = ChartCard(self.scroll_frame, "Order Status Breakdown")
        self.order_status_chart.grid(row=2, column=2, padx=12, pady=(0, 18), sticky="nsew")

        self.payment_status_chart = ChartCard(self.scroll_frame, "Payment Status Breakdown")
        self.payment_status_chart.grid(row=2, column=3, padx=(12, 24), pady=(0, 18), sticky="nsew")

    def _build_table_section(self):
        self.low_stock_table = TableCard(
            self.scroll_frame,
            "Low Stock Products",
            ("product", "quantity", "reorder_level", "status"),
            [
                ("product", "Product", 220),
                ("quantity", "Quantity", 90),
                ("reorder_level", "Reorder", 90),
                ("status", "Status", 110),
            ]
        )
        self.low_stock_table.grid(row=3, column=0, columnspan=2, padx=(24, 12), pady=(0, 24), sticky="nsew")

        self.recent_orders_table = TableCard(
            self.scroll_frame,
            "Recent Orders",
            ("order_id", "customer", "amount", "status"),
            [
                ("order_id", "Order ID", 90),
                ("customer", "Customer", 220),
                ("amount", "Amount", 100),
                ("status", "Status", 120),
            ]
        )
        self.recent_orders_table.grid(row=3, column=2, columnspan=2, padx=(12, 24), pady=(0, 24), sticky="nsew")

    def _fetch_rows(self, query, params=None):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def _fetch_one(self, query, params=None):
        rows = self._fetch_rows(query, params)
        return rows[0] if rows else None

    def _format_currency(self, amount):
        return f"Rs {float(amount):,.2f}"

    def _load_metrics(self):
        row = self._fetch_one(
            """
            SELECT
                (SELECT COUNT(*) FROM Products) AS total_products,
                (SELECT COUNT(*) FROM Customers) AS total_customers,
                (SELECT COUNT(*) FROM Orders) AS total_orders,
                (SELECT COUNT(*) FROM Payments) AS total_payments,
                (SELECT COUNT(*) FROM Suppliers) AS total_suppliers,
                (SELECT COUNT(*) FROM Inventory WHERE Quantity <= ReorderLevel) AS low_stock,
                (SELECT COUNT(*) FROM Orders WHERE OrderStatus = 'Pending') AS pending_orders,
                (SELECT ISNULL(SUM(Amount), 0) FROM Payments WHERE PaymentStatus = 'Completed') AS revenue
            """
        )

        return {
            "Products": (row.total_products, "#3B82F6", "Active catalog items"),
            "Customers": (row.total_customers, "#10B981", "Registered buyers"),
            "Orders": (row.total_orders, "#F59E0B", "All recorded orders"),
            "Revenue": (self._format_currency(row.revenue), "#EF4444", "Completed payments only"),
            "Payments": (row.total_payments, "#06B6D4", "Captured payment records"),
            "Low Stock": (row.low_stock, "#F97316", "Needs reorder attention"),
            "Pending Orders": (row.pending_orders, "#A78BFA", "Awaiting action"),
            "Suppliers": (row.total_suppliers, "#22C55E", "Active vendor records"),
        }

    def _load_sales_trend(self):
        rows = self._fetch_rows(
            """
            SELECT
                CONVERT(date, PaymentDate) AS payment_day,
                SUM(Amount) AS revenue
            FROM Payments
            WHERE PaymentStatus = 'Completed'
            GROUP BY CONVERT(date, PaymentDate)
            ORDER BY payment_day DESC
            """
        )

        latest_rows = list(reversed(rows[:7]))
        return [
            (row.payment_day.strftime("%d %b"), float(row.revenue or 0))
            for row in latest_rows
        ]

    def _load_order_status(self):
        rows = self._fetch_rows(
            """
            SELECT
                OrderStatus,
                COUNT(*) AS total_count
            FROM Orders
            GROUP BY OrderStatus
            ORDER BY total_count DESC, OrderStatus
            """
        )
        return [(row.OrderStatus, row.total_count) for row in rows]

    def _load_payment_status(self):
        rows = self._fetch_rows(
            """
            SELECT
                PaymentStatus,
                COUNT(*) AS total_count
            FROM Payments
            GROUP BY PaymentStatus
            ORDER BY total_count DESC, PaymentStatus
            """
        )
        return [(row.PaymentStatus, row.total_count) for row in rows]

    def _load_low_stock(self):
        rows = self._fetch_rows(
            """
            SELECT TOP 10
                P.ProductName,
                I.Quantity,
                I.ReorderLevel
            FROM Inventory AS I
            INNER JOIN Products AS P
                ON I.ProductID = P.ProductID
            WHERE I.Quantity <= I.ReorderLevel
            ORDER BY I.Quantity ASC, P.ProductName
            """
        )

        return [
            (
                row.ProductName,
                row.Quantity,
                row.ReorderLevel,
                "LOW STOCK",
            )
            for row in rows
        ]

    def _load_recent_orders(self):
        rows = self._fetch_rows(
            """
            SELECT TOP 10
                O.OrderID,
                C.FirstName,
                C.LastName,
                O.TotalAmount,
                O.OrderStatus
            FROM Orders AS O
            INNER JOIN Customers AS C
                ON O.CustomerID = C.CustomerID
            ORDER BY O.OrderDate DESC, O.OrderID DESC
            """
        )

        return [
            (
                row.OrderID,
                f"{row.FirstName} {row.LastName or ''}".strip(),
                self._format_currency(row.TotalAmount or 0),
                row.OrderStatus,
            )
            for row in rows
        ]

    def _render_metric_cards(self, metrics):
        for widget in self.metric_frame.winfo_children():
            widget.destroy()

        row = 0
        column = 0

        for title, (value, color, note) in metrics.items():
            card = MetricCard(self.metric_frame, title, str(value), color, note)
            card.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

            column += 1
            if column == 4:
                column = 0
                row += 1

    def refresh_dashboard(self):
        try:
            metrics = self._load_metrics()
            sales_trend = self._load_sales_trend()
            order_status = self._load_order_status()
            payment_status = self._load_payment_status()
            low_stock = self._load_low_stock()
            recent_orders = self._load_recent_orders()

            self._render_metric_cards(metrics)
            self.sales_chart.draw_line_chart(sales_trend)
            self.order_status_chart.draw_bar_chart(order_status, "#F59E0B")
            self.payment_status_chart.draw_bar_chart(payment_status, "#06B6D4")
            self.low_stock_table.populate(low_stock)
            self.recent_orders_table.populate(recent_orders)

            refreshed_at = datetime.now().strftime("%d %b %Y %I:%M %p")
            self.summary_var.set(f"Live business snapshot refreshed at {refreshed_at}")
        except Exception as error:
            self.summary_var.set(f"Failed to load dashboard: {error}")
