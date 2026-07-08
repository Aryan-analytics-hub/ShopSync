from database import get_connection

def view_products(): 

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            ProductID, 
            ProductName, 
            CostPrice, 
            SellingPrice
        FROM Products
        ORDER BY ProductID
    """)

    products = cursor.fetchall()
    print("\n===================== PRODUCTS =================\n")
    for product in products:
        print(
            f"{product.ProductID} |"
            f"{product.ProductName} |"
            f"₹{product.CostPrice} |"
            f"₹{product.SellingPrice}"
        )
    cursor.close()
    conn.close()


# =================================ADD function=============================

from database import get_connection

def add_product():
    conn = get_connection()
    cursor = conn.cursor()

    product_name = input("Enter Product Name: ")
    cost_price = float(input("Enter Cost Price: "))
    selling_price = float(input("Enter Selling Price: "))
    print("\n========== AVAILABLE SUPPLIERS ==========\n")

    cursor.execute("""
        SELECT
           SupplierID,
           SupplierName
        FROM Suppliers
        ORDER BY SupplierID
    """)

    suppliers = cursor.fetchall()

    for supplier in suppliers:

        print(
        f"{supplier.SupplierID} | "
        f"{supplier.SupplierName}"
    )

    print()
    supplier_id = int(input("Enter Supplier ID: "))
    
    print("\n========== AVAILABLE CATEGORIES ==========\n")
    cursor.execute("""
        SELECT
             CategoryID,
             CategoryName
        FROM Categories
        ORDER BY CategoryID
    """)
    categories = cursor.fetchall()
    for category in categories:
         print( 
              f"{category.CategoryID} | "
              f"{category.CategoryName}"
         )
    print()
    category_id = int(input("Enter Category ID: "))

    cursor.execute("""
        INSERT INTO Products
        (
            ProductName,
            CostPrice,
            SellingPrice,
            SupplierID,
            CategoryID
        )
        VALUES (?, ?, ?, ?, ?)
    """,
    (
        product_name,
        cost_price,
        selling_price,
        supplier_id,
        category_id
    ))

    conn.commit()

    print("\n✅ Product Added Successfully.")

    cursor.close()
    conn.close()


# =========================SEARCH FUNCTION=====================

def search_product():
     conn = get_connection()
     cursor = conn.cursor()

     product_name = input("Enter Product Name: ")

     cursor.execute(
            """
            SELECT
                ProductID,
                ProductName,
                CostPrice,
                SellingPrice
            FROM Products
            WHERE ProductName LIKE ?
            """,
            ('%' + product_name + '%',)
        )

     products = cursor.fetchall()

     if len(products) == 0:

            print("\nNo Product Found.")

     else:
        print("\n========== SEARCH RESULTS ==========\n")

        for product in products:

                print(
                    f"{product.ProductID} | "
                    f"{product.ProductName} | "
                    f"₹{product.CostPrice} | "
                    f"₹{product.SellingPrice}"
                )

     cursor.close()
     conn.close()


# ================================Update Product======================================
def update_product():

    conn = get_connection()
    cursor = conn.cursor()

    product_id = int(input("Enter Product ID to Update: "))

    cursor.execute(
        """
        SELECT ProductID
        FROM Products
        WHERE ProductID = ?
        """,
        product_id
    )

    product = cursor.fetchone()

    if product is None:

        print("\n❌ Product Not Found.")

    else:

        product_name = input("Enter New Product Name: ")
        cost_price = float(input("Enter New Cost Price: "))
        selling_price = float(input("Enter New Selling Price: "))
        supplier_id = int(input("Enter New Supplier ID: "))
        category_id = int(input("Enter New Category ID: "))

        cursor.execute(
            """
            UPDATE Products
            SET
                ProductName = ?,
                CostPrice = ?,
                SellingPrice = ?,
                SupplierID = ?,
                CategoryID = ?
            WHERE ProductID = ?
            """,
            (
                product_name,
                cost_price,
                selling_price,
                supplier_id,
                category_id,
                product_id
            )
        )

        conn.commit()

        print("\n✅ Product Updated Successfully.")

    cursor.close()
    conn.close()
       


# =======================Delete Function============================
# ======================== DELETE FUNCTION =======================

def delete_product():

    conn = get_connection()
    cursor = conn.cursor()

    product_id = int(input("Enter Product ID to Delete: "))

    cursor.execute(
        """
        DELETE FROM Products
        WHERE ProductID = ?
        """,
        (product_id,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        print("\n❌ Product Not Found.")

    else:
        print("\n✅ Product Deleted Successfully.")

    cursor.close()
    conn.close()