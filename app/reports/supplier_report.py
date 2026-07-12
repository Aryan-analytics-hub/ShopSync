from database import get_connection
from utils.display import print_header


def supplier_report():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            S.SupplierID,
            S.SupplierName,
            COUNT(P.ProductID) AS ProductsSupplied

        FROM Suppliers S

        LEFT JOIN Products P
            ON S.SupplierID = P.SupplierID

        GROUP BY

            S.SupplierID,
            S.SupplierName

        ORDER BY ProductsSupplied DESC
    """)

    suppliers = cursor.fetchall()

    print_header("SUPPLIER REPORT")

    print(
        f"{'ID':<6}"
        f"{'Supplier':<40}"
        f"{'Products Supplied'}"
    )

    print("-" * 65)

    for supplier in suppliers:

        print(
            f"{supplier.SupplierID:<6}"
            f"{supplier.SupplierName:<40}"
            f"{supplier.ProductsSupplied}"
        )

    cursor.close()
    conn.close()