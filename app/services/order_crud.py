from database import get_connection


def view_orders():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            OrderID,
            CustomerID,
            OrderDate,
            TotalAmount,
            OrderStatus
        FROM Orders
        ORDER BY OrderID
    """)

    orders = cursor.fetchall()

    print("\n========== ORDERS ==========\n")

    for order in orders:

        print(
            f"{order.OrderID} | "
            f"Customer ID: {order.CustomerID} | "
            f"{order.OrderDate} | "
            f"₹{order.TotalAmount} | "
            f"{order.OrderStatus}"
        )

    cursor.close()
    conn.close()


def add_order():

    conn = get_connection()
    cursor = conn.cursor()

    print("\n========== AVAILABLE CUSTOMERS ==========\n")

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

    customer_id = int(input("Enter Customer ID: "))
    total_amount = float(input("Enter Total Amount: "))
    order_status = input("Enter Order Status: ")

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
        total_amount,
        order_status
    ))

    conn.commit()

    print("\n✅ Order Added Successfully.")

    cursor.close()
    conn.close()


def search_order():

    conn = get_connection()
    cursor = conn.cursor()

    order_id = int(input("Enter Order ID: "))

    cursor.execute("""
        SELECT
            OrderID,
            CustomerID,
            OrderDate,
            TotalAmount,
            OrderStatus
        FROM Orders
        WHERE OrderID = ?
    """,
    (order_id,)
    )

    order = cursor.fetchone()

    if order is None:

        print("\n❌ Order Not Found.")

    else:

        print("\n========== ORDER ==========\n")

        print(
            f"{order.OrderID} | "
            f"Customer ID: {order.CustomerID} | "
            f"{order.OrderDate} | "
            f"₹{order.TotalAmount} | "
            f"{order.OrderStatus}"
        )

    cursor.close()
    conn.close()


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

        status = input("Enter New Order Status: ")

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