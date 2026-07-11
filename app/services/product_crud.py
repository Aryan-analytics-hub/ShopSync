import pyodbc
from database import get_connection
from utils.exception_handler import handle_database_error
from utils.display import (
    
    print_header,
    show_suppliers,
    show_categories
)

def view_products(): 

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            P.ProductID,
            P.ProductName,
            P.Description,

            C.CategoryName,

            S.SupplierName,

            P.CostPrice,
            P.SellingPrice

        FROM Products AS P

        INNER JOIN Categories AS C
            ON P.CategoryID = C.CategoryID

        INNER JOIN Suppliers AS S
            ON P.SupplierID = S.SupplierID

        ORDER BY P.ProductID
    """)

    products = cursor.fetchall()
    print_header("Products")
    print("ID | Product | Description | Category | Supplier | Cost | Selling")
    print("-"*90)
    for product in products:
        print(
            f"{product.ProductID} | "
            f"{product.Description} | "
            f"{product.ProductName} | "
            f"{product.CategoryName} | "
            f"{product.SupplierName} | "
            f"₹{product.CostPrice} | "
            f"₹{product.SellingPrice}"
        )
    cursor.close()
    conn.close()


    # =================================ADD function=============================
def add_product():

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        print_header("Add Product")

        product_name = input("Enter Product Name: ").strip()
        description = input("Enter Product Description: ").strip()

        cost_price = float(input("Enter Cost Price: "))
        selling_price = float(input("Enter Selling Price: "))
        

        show_suppliers()
        supplier_id = int(input("Enter Supplier ID: "))

        show_categories()
        category_id = int(input("Enter Category ID: "))

        cursor.execute("""
            INSERT INTO Products
            (
                ProductName,
                Description,
                CostPrice,
                SellingPrice,
                SupplierID,
                CategoryID
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            product_name,
            description,
            cost_price,
            selling_price,
            supplier_id,
            category_id
        ))

        conn.commit()
        # Get newly created Product ID

        cursor.execute("""
            SELECT CAST(SCOPE_IDENTITY() AS INT)
        """)

        product_id = cursor.fetchone()[0]

        # Automatically create Inventory record

        # cursor.execute("""
        #     INSERT INTO Inventory
        #     (
        #         ProductID,
        #         Quantity,
        #         ReorderLevel
        #     )
        #     VALUES (?, ?, ?)
        # """,
        # (
        #     product_id,
        #     0,
        #     10
        # ))

        # conn.commit()

        print("\n✅ Product Added Successfully.")

    except ValueError:

        print("\n❌ Invalid input. Please enter numeric values where required.")

    except pyodbc.IntegrityError as e:

        print("\n❌ Database Error")
        print(e)

        print("- Supplier ID does not exist.")
        print("- Category ID does not exist.")
        print("- Selling Price violates database rules.")
        print("- Product data violates a database constraint.")

    except Exception as e:

        print(f"\n❌ Unexpected Error: {e}")

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()
# =========================SEARCH FUNCTION=====================

def search_product():

    conn = get_connection()
    cursor = conn.cursor()

    product_name = input("Enter Product Name: ")

    cursor.execute("""
        SELECT

            P.ProductID,
            P.ProductName,
            P.Description,

            C.CategoryName,

            S.SupplierName,

            P.CostPrice,
            P.SellingPrice

        FROM Products AS P

        INNER JOIN Categories AS C
            ON P.CategoryID = C.CategoryID

        INNER JOIN Suppliers AS S
            ON P.SupplierID = S.SupplierID

        WHERE P.ProductName LIKE ?

        ORDER BY P.ProductID
    """,
    ('%' + product_name + '%',)
    )

    products = cursor.fetchall()

    if len(products) == 0:

        print("\n❌ No Product Found.")

    else:

        print_header("Search Results")

        print("ID | Product | Description | Category | Supplier | Cost | Selling")
        print("-" * 120)

        for product in products:

            print(
                f"{product.ProductID} | "
                f"{product.ProductName} | "
                f"{product.Description} | "
                f"{product.CategoryName} | "
                f"{product.SupplierName} | "
                f"₹{product.CostPrice} | "
                f"₹{product.SellingPrice}"
            )

    cursor.close()
    conn.close()
# ================================Update Product======================================
def update_product():

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        print_header("Update Product")

        product_id = int(input("Enter Product ID to Update: "))

        cursor.execute("""
            SELECT ProductID
            FROM Products
            WHERE ProductID = ?
        """,
        (product_id,)
        )

        product = cursor.fetchone()

        if product is None:

            print("\n❌ Product Not Found.")

            return

        product_name = input("Enter New Product Name: ").strip()

        description = input("Enter New Description: ").strip()

        cost_price = float(input("Enter New Cost Price: "))
        selling_price = float(input("Enter New Selling Price: "))

        show_suppliers()
        supplier_id = int(input("Enter New Supplier ID: "))

        show_categories()
        category_id = int(input("Enter New Category ID: "))

        cursor.execute("""
            UPDATE Products
            SET
                ProductName = ?,
                Description = ?,
                CostPrice = ?,
                SellingPrice = ?,
                SupplierID = ?,
                CategoryID = ?
            WHERE ProductID = ?
        """,
        (
            product_name,
            description,
            cost_price,
            selling_price,
            supplier_id,
            category_id,
            product_id
        ))

        conn.commit()

        print("\n✅ Product Updated Successfully.")

    except ValueError:

        print("\n❌ Invalid input. Please enter valid numeric values.")

    except pyodbc.IntegrityError:

        print("\n❌ Database Error.")

        print("Possible reasons:")

        print("- Supplier ID does not exist.")
        print("- Category ID does not exist.")
        print("- Invalid product data.")

    except Exception as e:

        print(f"\n❌ Unexpected Error: {e}")

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ======================== DELETE FUNCTION =======================

def delete_product():

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        print_header("Delete Product")

        product_id = int(input("Enter Product ID to Delete: "))

        cursor.execute("""
            SELECT ProductID
            FROM Products
            WHERE ProductID = ?
        """,
        (product_id,)
        )

        product = cursor.fetchone()

        if product is None:

            print("\n❌ Product Not Found.")

            return

        cursor.execute("""
            DELETE FROM Products
            WHERE ProductID = ?
        """,
        (product_id,)
        )

        conn.commit()

        print("\n✅ Product Deleted Successfully.")

    except ValueError:

        print("\n❌ Invalid Product ID.")

    except pyodbc.IntegrityError:

        print("\n❌ Cannot delete this product.")

        print("Possible reasons:")

        print("- Product exists in Inventory.")
        print("- Product exists in Order Items.")
        print("- Product is referenced by another table.")

    except Exception as e:

        print(f"\n❌ Unexpected Error: {e}")

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()