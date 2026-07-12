from database import get_connection
from utils.display import print_header


def inventory_report():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            P.ProductName,
            I.Quantity,
            I.ReorderLevel

        FROM Inventory I

        INNER JOIN Products P
            ON I.ProductID = P.ProductID

        ORDER BY P.ProductName
    """)

    items = cursor.fetchall()

    print_header("INVENTORY REPORT")

    print(
        f"{'Product':<35}"
        f"{'Quantity':<12}"
        f"{'Reorder':<12}"
        f"{'Status'}"
    )

    print("-" * 75)

    for item in items:

        status = "LOW STOCK" if item.Quantity <= item.ReorderLevel else "IN STOCK"

        print(
            f"{item.ProductName:<35}"
            f"{item.Quantity:<12}"
            f"{item.ReorderLevel:<12}"
            f"{status}"
        )

    cursor.close()
    conn.close()