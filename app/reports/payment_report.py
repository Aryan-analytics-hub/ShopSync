from database import get_connection
from utils.display import print_header


def payment_report():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            P.PaymentID,
            P.OrderID,
            C.FirstName,
            C.LastName,
            P.PaymentMethod,
            P.Amount,
            P.PaymentStatus

        FROM Payments P

        INNER JOIN Orders O
            ON P.OrderID = O.OrderID

        INNER JOIN Customers C
            ON O.CustomerID = C.CustomerID

        ORDER BY P.PaymentID DESC
    """)

    payments = cursor.fetchall()

    print_header("PAYMENT REPORT")

    print(
        f"{'Payment':<10}"
        f"{'Order':<10}"
        f"{'Customer':<25}"
        f"{'Method':<18}"
        f"{'Amount':<15}"
        f"{'Status'}"
    )

    print("-" * 100)

    for payment in payments:

        customer = f"{payment.FirstName} {payment.LastName}"

        print(
            f"{payment.PaymentID:<10}"
            f"{payment.OrderID:<10}"
            f"{customer:<25}"
            f"{payment.PaymentMethod:<18}"
            f"₹{payment.Amount:<13}"
            f"{payment.PaymentStatus}"
        )

    cursor.close()
    conn.close()