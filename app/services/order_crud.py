from database import get_connection
from utils.display import show_customers, print_header


def view_orders():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            O.OrderID,

            C.FirstName,

            C.LastName,

            O.OrderDate,

            O.TotalAmount,

            O.OrderStatus

        FROM Orders AS O

        INNER JOIN Customers AS C
            ON O.CustomerID = C.CustomerID

        ORDER BY O.OrderID
    """)

    orders = cursor.fetchall()

    print_header("Orders")

    print("Order ID | Customer | Date | Total | Status")
    print("-" * 90)

    for order in orders:

        print(
            f"{order.OrderID} | "
            f"{order.FirstName} {order.LastName} | "
            f"{order.OrderDate} | "
            f"₹{order.TotalAmount} | "
            f"{order.OrderStatus}"
        )

    cursor.close()
    conn.close()


# =========================================================


def add_order():

    conn = get_connection()
    cursor = conn.cursor()

    show_customers()

    customer_id = int(input("Enter Customer ID: "))

    print("\nAvailable Status")
    print("Pending")
    print("Confirmed")
    print("Packed")
    print("Shipped")
    print("Delivered")
    print("Cancelled")

    order_status = input("\nEnter Order Status: ")

    cursor.execute("""
        INSERT INTO Orders
        (
            CustomerID,
            TotalAmount,
            OrderStatus
        )
        VALUES (?, ?, ?)
    """,
    (
        customer_id,
        0,
        order_status
    ))

    conn.commit()

    print("\n✅ Order Created Successfully.")
    print("Total Amount = ₹0")
    print("Now add products using Order Item Management.")

    cursor.close()
    conn.close()


# =========================================================


def search_order():

    conn = get_connection()
    cursor = conn.cursor()

    order_id = int(input("Enter Order ID: "))

    cursor.execute("""
        SELECT

            O.OrderID,

            C.FirstName,

            C.LastName,

            O.OrderDate,

            O.TotalAmount,

            O.OrderStatus

        FROM Orders AS O

        INNER JOIN Customers AS C
            ON O.CustomerID = C.CustomerID

        WHERE O.OrderID = ?

        ORDER BY O.OrderID
    """,
    (order_id,)
    )

    order = cursor.fetchone()

    if order is None:

        print("\n❌ Order Not Found.")

    else:

        print_header("Order")

        print(
            f"Order ID : {order.OrderID}"
        )

        print(
            f"Customer : {order.FirstName} {order.LastName}"
        )

        print(
            f"Date     : {order.OrderDate}"
        )

        print(
            f"Total    : ₹{order.TotalAmount}"
        )

        print(
            f"Status   : {order.OrderStatus}"
        )

    cursor.close()
    conn.close()


# =========================================================


def update_order():

    conn = get_connection()
    cursor = conn.cursor()

    order_id = int(input("Enter Order ID: "))

    cursor.execute("""
        SELECT OrderID
        FROM Orders
        WHERE OrderID = ?
    """,
    (order_id,)
    )

    order = cursor.fetchone()

    if order is None:

        print("\n❌ Order Not Found.")

    else:

        print("\nAvailable Status")

        print("Pending")
        print("Confirmed")
        print("Packed")
        print("Shipped")
        print("Delivered")
        print("Cancelled")

        status = input("\nEnter New Status: ")

        cursor.execute("""
            UPDATE Orders
            SET OrderStatus = ?
            WHERE OrderID = ?
        """,
        (
            status,
            order_id
        ))

        conn.commit()

        print("\n✅ Order Updated Successfully.")

    cursor.close()
    conn.close()


# =========================================================


def delete_order():

    conn = get_connection()
    cursor = conn.cursor()

    order_id = int(input("Enter Order ID: "))

    cursor.execute("""
        SELECT OrderID
        FROM Orders
        WHERE OrderID = ?
    """,
    (order_id,)
    )

    order = cursor.fetchone()

    if order is None:

        print("\n❌ Order Not Found.")

    else:

        cursor.execute("""
            DELETE FROM Orders
            WHERE OrderID = ?
        """,
        (order_id,)
        )

        conn.commit()

        print("\n✅ Order Deleted Successfully.")

    cursor.close()
    conn.close()