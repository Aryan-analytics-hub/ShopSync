from faker import Faker
from random import randint

from database import get_connection

fake = Faker()


def insert_order_items(num_items):

    conn = get_connection()
    cursor = conn.cursor()

    order_count = cursor.execute(
        "SELECT COUNT(*) FROM Orders"
    ).fetchone()[0]

    product_count = cursor.execute(
        "SELECT COUNT(*) FROM Products"
    ).fetchone()[0]

    for _ in range(num_items):

        order_id = randint(1001, 1000 + order_count)

        product_id = randint(1, product_count)

        quantity = randint(1, 5)

        unit_price = cursor.execute(
            """
            SELECT SellingPrice
            FROM Products
            WHERE ProductID = ?
            """,
            product_id
        ).fetchone()[0]

        cursor.execute(
            """
            INSERT INTO OrderItems
            (
                OrderID,
                ProductID,
                Quantity,
                UnitPrice
            )
            VALUES
            (
                ?, ?, ?, ?
            )
            """,
            (
                order_id,
                product_id,
                quantity,
                unit_price
            )
        )

    conn.commit()

    cursor.close()
    conn.close()

    print("✅ OrderItems inserted successfully.")