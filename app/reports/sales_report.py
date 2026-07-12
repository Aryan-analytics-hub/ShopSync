
from database import get_connection
from utils.display import print_header


def sales_report():

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

        ORDER BY O.OrderID DESC
    """)

    orders = cursor.fetchall()

    print_header("SALES REPORT")

    print(
        f"{'Order ID':<10}"
        f"{'Customer':<25}"
        f"{'Date':<25}"
        f"{'Amount':<15}"
        f"{'Status'}"
    )

    print("-" * 90)

    for order in orders:

        customer = f"{order.FirstName} {order.LastName}"

        print(
            f"{order.OrderID:<10}"
            f"{customer:<25}"
            f"{str(order.OrderDate):<25}"
            f"₹{order.TotalAmount:<13}"
            f"{order.OrderStatus}"
        )

    cursor.close()
    conn.close()