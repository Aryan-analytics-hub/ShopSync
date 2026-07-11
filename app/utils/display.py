from database import get_connection


def print_header(title):

    print(f"\n========== {title.upper()} ==========\n")

    from database import get_connection


def show_products():

    conn = get_connection()
    cursor = conn.cursor()

    print_header("Available Products")

    cursor.execute("""
        SELECT
            ProductID,
            ProductName
        FROM Products
        ORDER BY ProductID
    """)

    products = cursor.fetchall()

    for product in products:

        print(
            f"{product.ProductID} | "
            f"{product.ProductName}"
        )

    print()

    cursor.close()
    conn.close()


def show_customers():

    conn = get_connection()
    cursor = conn.cursor()

    print_header("Available Customers")

    cursor.execute("""
        SELECT
            CustomerID,
            FirstName,
            LastName
        FROM Customers
        ORDER BY CustomerID
    """)

    customers = cursor.fetchall()

    for customer in customers:

        print(
            f"{customer.CustomerID} | "
            f"{customer.FirstName} {customer.LastName}"
        )

    print()

    cursor.close()
    conn.close()


def show_suppliers():

    conn = get_connection()
    cursor = conn.cursor()

    print_header("Available Suppliers")

    cursor.execute("""
        SELECT
            SupplierID,
            SupplierName
        FROM Suppliers
        ORDER BY SupplierID
    """)

    suppliers = cursor.fetchall()

    for supplier in suppliers:

        print(
            f"{supplier.SupplierID} | "
            f"{supplier.SupplierName}"
        )

    print()

    cursor.close()
    conn.close()

def show_categories():

    conn = get_connection()
    cursor = conn.cursor()

    print_header("Available Categories")

    cursor.execute("""
        SELECT
            CategoryID,
            CategoryName
        FROM Categories
        ORDER BY CategoryID
    """)

    categories = cursor.fetchall()

    for category in categories:

        print(
            f"{category.CategoryID} | "
            f"{category.CategoryName}"
        )

    print()

    cursor.close()
    conn.close()


def show_orders():

    conn = get_connection()
    cursor = conn.cursor()

    print_header("Available Orders")

    cursor.execute("""
        SELECT
            OrderID
        FROM Orders
        ORDER BY OrderID
    """)

    orders = cursor.fetchall()

    for order in orders:

        print(order.OrderID)

    print()

    cursor.close()
    conn.close()