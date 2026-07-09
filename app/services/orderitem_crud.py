from database import get_connection


def view_order_items():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            OrderItemID,
            OrderID,
            ProductID,
            Quantity,
            UnitPrice,
            SubTotal
        FROM OrderItems
        ORDER BY OrderItemID
    """)

    order_items = cursor.fetchall()

    print("\n========== ORDER ITEMS ==========\n")

    for item in order_items:

        print(
            f"{item.OrderItemID} | "
            f"Order ID: {item.OrderID} | "
            f"Product ID: {item.ProductID} | "
            f"Qty: {item.Quantity} | "
            f"₹{item.UnitPrice} | "
            f"Subtotal: ₹{item.SubTotal}"
        )

    cursor.close()
    conn.close()


def add_order_item():

    conn = get_connection()
    cursor = conn.cursor()

    print("\n========== AVAILABLE ORDERS ==========\n")

    cursor.execute("""
        SELECT
            OrderID
        FROM Orders
        ORDER BY OrderID
    """)

    orders = cursor.fetchall()

    for order in orders:

        print(order.OrderID)

    print("\n========== AVAILABLE PRODUCTS ==========\n")

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

    order_id = int(input("Enter Order ID: "))
    product_id = int(input("Enter Product ID: "))
    quantity = int(input("Enter Quantity: "))
    unit_price = float(input("Enter Unit Price: "))

    cursor.execute("""
        INSERT INTO OrderItems
        (
            OrderID,
            ProductID,
            Quantity,
            UnitPrice
        )
        VALUES (?, ?, ?, ?)
    """,
    (
        order_id,
        product_id,
        quantity,
        unit_price
    ))

    conn.commit()

    print("\n✅ Order Item Added Successfully.")

    cursor.close()
    conn.close()


def search_order_item():

    conn = get_connection()
    cursor = conn.cursor()

    order_item_id = int(input("Enter Order Item ID: "))

    cursor.execute("""
        SELECT
            OrderItemID,
            OrderID,
            ProductID,
            Quantity,
            UnitPrice,
            SubTotal
        FROM OrderItems
        WHERE OrderItemID = ?
    """,
    (order_item_id,)
    )

    item = cursor.fetchone()

    if item is None:

        print("\n❌ Order Item Not Found.")

    else:

        print("\n========== ORDER ITEM ==========\n")

        print(
            f"{item.OrderItemID} | "
            f"Order ID: {item.OrderID} | "
            f"Product ID: {item.ProductID} | "
            f"Qty: {item.Quantity} | "
            f"₹{item.UnitPrice} | "
            f"Subtotal: ₹{item.SubTotal}"
        )

    cursor.close()
    conn.close()


def update_order_item():

    conn = get_connection()
    cursor = conn.cursor()

    order_item_id = int(input("Enter Order Item ID: "))

    cursor.execute("""
        SELECT OrderItemID
        FROM OrderItems
        WHERE OrderItemID = ?
    """,
    (order_item_id,)
    )

    item = cursor.fetchone()

    if item is None:

        print("\n❌ Order Item Not Found.")

    else:

        quantity = int(input("Enter New Quantity: "))
        unit_price = float(input("Enter New Unit Price: "))

        cursor.execute("""
            UPDATE OrderItems
            SET
                Quantity = ?,
                UnitPrice = ?
            WHERE OrderItemID = ?
        """,
        (
            quantity,
            unit_price,
            order_item_id
        ))

        conn.commit()

        print("\n✅ Order Item Updated Successfully.")

    cursor.close()
    conn.close()


def delete_order_item():

    conn = get_connection()
    cursor = conn.cursor()

    order_item_id = int(input("Enter Order Item ID: "))

    cursor.execute("""
        SELECT OrderItemID
        FROM OrderItems
        WHERE OrderItemID = ?
    """,
    (order_item_id,)
    )

    item = cursor.fetchone()

    if item is None:

        print("\n❌ Order Item Not Found.")

    else:

        cursor.execute("""
            DELETE FROM OrderItems
            WHERE OrderItemID = ?
        """,
        (order_item_id,)
        )

        conn.commit()

        print("\n✅ Order Item Deleted Successfully.")

    cursor.close()
    conn.close()