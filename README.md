# 🛒 ShopSync – Inventory Management System

A modern desktop-based **Inventory Management System** developed using **Python**, **CustomTkinter**, and **Microsoft SQL Server**.

ShopSync streamlines inventory management by providing product tracking, customer and supplier management, order processing, analytics dashboards, reporting, and secure authentication—all within an intuitive desktop application.

---

## 📌 Features

### 🔐 Authentication
- Secure login system
- Admin account initialization
- User authentication service

### 📊 Dashboard
- Business overview
- Key Performance Indicators (KPIs)
- Revenue summary
- Inventory statistics
- Quick navigation

### 📦 Inventory Management
- Product Management
- Category Management
- Inventory Tracking
- Stock Updates

### 👥 Customer Management
- Add customers
- Update customer details
- Search customers
- Delete customers

### 🚚 Supplier Management
- Supplier database
- Contact information
- Supplier search

### 🛍 Order Management
- Create Orders
- Order Items
- Payment Tracking
- Billing Support

### 📈 Analytics Dashboard
- Sales Analytics
- Inventory Analytics
- Product Insights
- Customer Insights
- Supplier Analytics
- Payment Analysis
- Business Recommendations
- Interactive Charts

### 📄 Reports
- Sales Reports
- Inventory Reports
- Customer Reports
- Supplier Reports
- Export to CSV
- Export to Excel (.xlsx)

---

# 🛠 Technologies Used

| Technology | Purpose |
|------------|----------|
| Python 3.13 | Programming Language |
| CustomTkinter | Modern Desktop GUI |
| SQL Server | Database |
| pyodbc | Database Connectivity |
| openpyxl | Excel Export |
| matplotlib | Data Visualization |
| tkinter | GUI Components |

---

# 📂 Project Structure

```
ShopSync/
│
├── app/
│   ├── assets/
│   ├── gui/
│   │   ├── pages/
│   │   ├── widgets/
│   │   ├── login.py
│   │   ├── sidebar.py
│   │   └── main_window.py
│   │
│   ├── services/
│   ├── dashboard/
│   ├── config.py
│   ├── config.ini
│   ├── main.py
│   └── requirements.txt
│
├── Database/
│
├── Documentation/
│
└── README.md
```

---

# 🚀 Major Modules

- Authentication
- Dashboard
- Categories
- Products
- Customers
- Suppliers
- Inventory
- Orders
- Payments
- Analytics
- Reports

---

# 📊 Analytics

The Analytics module provides:

- Sales Performance
- Revenue Insights
- Inventory Statistics
- Customer Analytics
- Supplier Analytics
- Payment Analysis
- Business Recommendations
- Interactive Visualizations

---

# 📄 Reports

Generate professional reports and export them in:

- CSV
- Microsoft Excel (.xlsx)

---

# 🔒 Database

Database: **Microsoft SQL Server**

Uses:

- Foreign Keys
- Primary Keys
- Normalized Tables
- Parameterized SQL Queries
- Windows Authentication Support

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/Aryan-analytics-hub/ShopSync.git
```

## Navigate

```bash
cd ShopSync/app
```

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🗄 Configure Database

Update:

```
app/config.ini
```

Example

```ini
[database]
server=localhost\SQLEXPRESS
database=ShopSyncDB
trusted_connection=yes
```

Import the SQL scripts from the **Database** folder before running the application.

---

# ▶ Run Application

```bash
python main.py
```

---

# 📸 Screenshots

> Add screenshots here after uploading them.

- Login Screen
- Dashboard
- Inventory
- Products
- Customers
- Reports
- Analytics

---

# 🎯 Future Improvements

- Barcode Scanner
- QR Code Support
- Email Notifications
- PDF Export
- Backup & Restore
- Multi-user Roles
- Cloud Database Support

---

# 📚 Learning Outcomes

This project demonstrates:

- Object-Oriented Programming
- Desktop Application Development
- SQL Server Integration
- Data Analytics
- Dashboard Design
- Authentication
- Excel Automation
- Software Architecture
- Modular Programming

---

# 👨‍💻 Author

**Aryan Kumar**

MCA Student

Aspiring Data Analyst | AI & Machine Learning Enthusiast

GitHub:
https://github.com/Aryan-analytics-hub

---

# ⭐ If you like this project

Please consider giving the repository a **Star ⭐**
