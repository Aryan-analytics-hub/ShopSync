from faker import Faker
from random import choice, randint

from database import get_connection

fake = Faker()


def insert_payments(num_payments):

    conn = get_connection()
    cursor = conn.cursor()

    order_count = cursor.execute(
        "SELECT COUNT(*) FROM Orders"
    ).fetchone()[0]

    payment_methods = [
        "Cash",
        "Card",
        "UPI",
        "Net Banking"
    ]

    payment_statuses = [
        "Pending",
        "Completed",
        "Failed",
        "Refunded"
    ]

    for _ in range(num_payments):

        order_id = randint(1001, 1000 + order_count)

        amount = cursor.execute(
            """
            SELECT TotalAmount
            FROM Orders
            WHERE OrderID = ?
            """,
            order_id
        ).fetchone()[0]

        cursor.execute(
            """
            INSERT INTO Payments
            (
                OrderID,
                PaymentDate,
                PaymentMethod,
                Amount,
                PaymentStatus,
                TransactionReference
            )
            VALUES
            (
                ?, ?, ?, ?, ?, ?
            )
            """,
            (
                order_id,
                fake.date_time_this_year(),
                choice(payment_methods),
                amount,
                choice(payment_statuses),
                fake.uuid4()
            )
        )

    conn.commit()

    cursor.close()
    conn.close()

    print("✅ Payments inserted successfully.")