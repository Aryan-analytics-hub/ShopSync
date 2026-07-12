from database import get_connection
from utils.display import print_header


def customer_report():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            C.CustomerID,
            C.FirstName,
            C.LastName,
            COUNT(O.OrderID) AS TotalOrders,
            ISNULL(SUM(O.TotalAmount),0) AS TotalSpent

        FROM Customers C

        LEFT JOIN Orders O
            ON C.CustomerID = O.CustomerID

        GROUP BY

            C.CustomerID,
            C.FirstName,
            C.LastName

        ORDER BY TotalSpent DESC
    """)

    customers = cursor.fetchall()

    print_header("CUSTOMER REPORT")

    print(
        f"{'ID':<6}"
        f"{'Customer':<30}"
        f"{'Orders':<12}"
        f"{'Total Spent'}"
    )

    print("-" * 70)

    for customer in customers:

        name = f"{customer.FirstName} {customer.LastName}"

        print(
            f"{customer.CustomerID:<6}"
            f"{name:<30}"
            f"{customer.TotalOrders:<12}"
            f"₹{customer.TotalSpent}"
        )

    cursor.close()
    conn.close()