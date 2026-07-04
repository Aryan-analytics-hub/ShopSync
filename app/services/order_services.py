from faker import Faker
from random import randint, choice

from database import get_connection

fake = Faker()


def insert_orders(num_orders):

    conn = get_connection()
    cursor = conn.cursor()

    customer_count = cursor.execute(
        "SELECT COUNT(*) FROM Customers"
    ).fetchone()[0]

    statuses = [
        "Pending",
        "Confirmed",
        "Packed",
        "Shipped",
        "Delivered",
        "Cancelled"
    ]

    for _ in range(num_orders):

        customer_id = randint(1, customer_count)

        order_date = fake.date_time_between(
            start_date="-1y",
            end_date="now"
        )

        total_amount = round(
            randint(500, 50000) + randint(0, 99) / 100,
            2
        )

        order_status = choice(statuses)

        cursor.execute("""
            INSERT INTO Orders
            (
                CustomerID,
                OrderDate,
                TotalAmount,
                OrderStatus
            )
            VALUES (?, ?, ?, ?)
        """,
        (
            customer_id,
            order_date,
            total_amount,
            order_status
        ))

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Orders inserted successfully.")