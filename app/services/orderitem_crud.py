from database import get_connection
from utils.display import show_orders, show_products, print_header


def view_order_items():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            OI.OrderItemID,

            OI.OrderID,

            P.ProductName,

            OI.Quantity,

            OI.UnitPrice,

            OI.SubTotal

        FROM OrderItems AS OI

        INNER JOIN Products AS P
            ON OI.ProductID = P.ProductID

        ORDER BY OI.OrderItemID
    """)

    order_items = cursor.fetchall()

    print_header("Order Items")

    print("ID | Order | Product | Qty | Unit Price | Subtotal")
    print("-" * 90)

    for item in order_items:

        print(
            f"{item.OrderItemID} | "
            f"Order: {item.OrderID} | "
            f"{item.ProductName} | "
            f"Qty: {item.Quantity} | "
            f"₹{item.UnitPrice} | "
            f"Subtotal: ₹{item.SubTotal}"
        )

    cursor.close()
    conn.close()


# ==========================================================


def add_order_item():

    conn = get_connection()
    cursor = conn.cursor()

    show_orders()
    show_products()

    order_id = int(input("\nEnter Order ID: "))
    product_id = int(input("Enter Product ID: "))
    quantity = int(input("Enter Quantity: "))

    # Check Available Stock
    cursor.execute("""
        SELECT Quantity
        FROM Inventory
        WHERE ProductID = ?
    """,
    (product_id,)
    )

    stock = cursor.fetchone()

    if stock is None:

        print("\n❌ Inventory record not found.")

        cursor.close()
        conn.close()

        return

    available_stock = stock.Quantity

    if quantity <= 0:

        print("\n❌ Quantity must be greater than zero.")

        cursor.close()
        conn.close()

        return


    if quantity > available_stock:

        print("\n❌ Not enough stock available.")

        print(f"Available Stock : {available_stock}")

        cursor.close()
        conn.close()

        return
    # Automatically fetch selling price

    cursor.execute("""
        SELECT SellingPrice
        FROM Products
        WHERE ProductID = ?
    """,
    (product_id,)
    )

    price = cursor.fetchone()

    if price is None:

        print("\n❌ Product Not Found.")

        cursor.close()
        conn.close()

        return

    unit_price = price.SellingPrice

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

    cursor.execute("""
    UPDATE Inventory
    SET Quantity = Quantity - ?
    WHERE ProductID = ?
    """,
    (
        quantity,
        product_id
    ))

    conn.commit()

    # Recalculate Order Total

    cursor.execute("""
        SELECT
            SUM(SubTotal) AS Total
        FROM OrderItems
        WHERE OrderID = ?
    """,
    (order_id,)
    )

    total = cursor.fetchone()

    cursor.execute("""
        UPDATE Orders
        SET TotalAmount = ?
        WHERE OrderID = ?
    """,
    (
        total.Total,
        order_id
    ))

    conn.commit()

    print("\n✅ Order Item Added Successfully.")
    print(f"Order Total Updated : ₹{total.Total}")

    cursor.close()
    conn.close()


# ==========================================================


def search_order_item():

    conn = get_connection()
    cursor = conn.cursor()

    order_item_id = int(input("Enter Order Item ID: "))

    cursor.execute("""
        SELECT

            OI.OrderItemID,

            OI.OrderID,

            P.ProductName,

            OI.Quantity,

            OI.UnitPrice,

            OI.SubTotal

        FROM OrderItems AS OI

        INNER JOIN Products AS P
            ON OI.ProductID = P.ProductID

        WHERE OI.OrderItemID = ?
    """,
    (order_item_id,)
    )

    item = cursor.fetchone()

    if item is None:

        print("\n❌ Order Item Not Found.")

    else:

        print_header("Order Item")

        print(
            f"{item.OrderItemID} | "
            f"Order: {item.OrderID} | "
            f"{item.ProductName} | "
            f"Qty: {item.Quantity} | "
            f"₹{item.UnitPrice} | "
            f"Subtotal: ₹{item.SubTotal}"
        )

    cursor.close()
    conn.close()


# ==========================================================


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


# ==========================================================


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