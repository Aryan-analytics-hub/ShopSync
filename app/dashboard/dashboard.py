from database import get_connection
from utils.display import print_header


def dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    print_header("SHOPSYNC DASHBOARD")
    print("="*45)

    # Total Products

    cursor.execute("SELECT COUNT(*) FROM Products")
    total_products = cursor.fetchone()[0]

    # Total Customers

    cursor.execute("SELECT COUNT(*) FROM Customers")
    total_customers = cursor.fetchone()[0]

    # Total Suppliers

    cursor.execute("SELECT COUNT(*) FROM Suppliers")
    total_suppliers = cursor.fetchone()[0]

    # Total Categories

    cursor.execute("SELECT COUNT(*) FROM Categories")
    total_categories = cursor.fetchone()[0]

    # Total Orders

    cursor.execute("SELECT COUNT(*) FROM Orders")
    total_orders = cursor.fetchone()[0]

    # Total Payments

    cursor.execute("SELECT COUNT(*) FROM Payments")
    total_payments = cursor.fetchone()[0]

    # Revenue

    cursor.execute("""
        SELECT ISNULL(SUM(Amount),0)
        FROM Payments
        WHERE PaymentStatus='Completed'
    """)

    revenue = cursor.fetchone()[0]

    # Pending Orders

    cursor.execute("""
        SELECT COUNT(*)
        FROM Orders
        WHERE OrderStatus='Pending'
    """)

    pending_orders = cursor.fetchone()[0]

    # Low Stock

    cursor.execute("""
        SELECT COUNT(*)
        FROM Inventory
        WHERE Quantity <= ReorderLevel
    """)

    low_stock = cursor.fetchone()[0]

    print(f"Total Products      : {total_products}")
    print(f"Total Customers     : {total_customers}")
    print(f"Total Suppliers     : {total_suppliers}")
    print(f"Total Categories    : {total_categories}")
    print(f"Total Orders        : {total_orders}")
    print(f"Total Payments      : {total_payments}")

    print("-" * 45)

    print(f"Total Revenue       : ₹{revenue:,.2f}")
    print(f"Pending Orders      : {pending_orders}")
    print(f"Low Stock Products  : {low_stock}")

    cursor.close()
    conn.close()