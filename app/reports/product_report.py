from database import get_connection
from utils.display import print_header


def product_report():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            P.ProductName,
            C.CategoryName,
            S.SupplierName,
            P.SellingPrice

        FROM Products P

        INNER JOIN Categories C
            ON P.CategoryID = C.CategoryID

        INNER JOIN Suppliers S
            ON P.SupplierID = S.SupplierID

        ORDER BY P.ProductName
    """)

    products = cursor.fetchall()

    print_header("PRODUCT REPORT")

    print(
        f"{'Product':<30}"
        f"{'Category':<20}"
        f"{'Supplier':<30}"
        f"{'Price'}"
    )

    print("-" * 100)

    for product in products:

        print(
            f"{product.ProductName:<30}"
            f"{product.CategoryName:<20}"
            f"{product.SupplierName:<30}"
            f"₹{product.SellingPrice}"
        )

    cursor.close()
    conn.close()