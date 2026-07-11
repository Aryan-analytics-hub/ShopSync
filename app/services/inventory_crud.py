from database import get_connection
from utils.display import show_products
from utils.display import print_header

def view_inventory():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            I.InventoryID,

            P.ProductName,

            I.Quantity,

            I.ReorderLevel,

            I.LastUpdated

        FROM Inventory AS I

        INNER JOIN Products AS P
            ON I.ProductID = P.ProductID

        ORDER BY I.InventoryID""")

    inventory = cursor.fetchall()

    print_header("INVENTORY")
    print("ID | Product | Quantity | Reorder | Last Updated")
    print("-" * 90)

    for item in inventory:

        print(
            f"{item.InventoryID} | "
            f"{item.ProductName} | "
            f"Qty: {item.Quantity} | "
            f"Reorder: {item.ReorderLevel} | "
            f"{item.LastUpdated}"
        )
    
    cursor.close()
    conn.close()


def add_inventory():

    conn = get_connection()
    cursor = conn.cursor()

    show_products()

    product_id = int(input("Enter Product ID: "))
    quantity = int(input("Enter Quantity: "))
    reorder_level = int(input("Enter Reorder Level: "))

    cursor.execute(
        """
        INSERT INTO Inventory
        (
            ProductID,
            Quantity,
            ReorderLevel
        )
        VALUES (?, ?, ?)
        """,
        (
            product_id,
            quantity,
            reorder_level
        )
    )

    conn.commit()

    print("\n✅ Inventory Added Successfully.")

    cursor.close()
    conn.close()


def search_inventory():

    conn = get_connection()
    cursor = conn.cursor()

    product_id = int(input("Enter Product ID: "))

    cursor.execute(
        """
        SELECT
            InventoryID,
            ProductID,
            Quantity,
            ReorderLevel,
            LastUpdated
        FROM Inventory
        WHERE ProductID = ?
        """,
        (product_id,)
    )

    item = cursor.fetchone()

    if item is None:

        print("\n❌ Inventory Record Not Found.")

    else:

        print("\n========== INVENTORY ==========\n")

        print(
            f"{item.InventoryID} | "
            f"Product ID: {item.ProductID} | "
            f"Qty: {item.Quantity} | "
            f"Reorder: {item.ReorderLevel} | "
            f"{item.LastUpdated}"
        )

    cursor.close()
    conn.close()


def update_inventory():

    conn = get_connection()
    cursor = conn.cursor()

    product_id = int(input("Enter Product ID to Update: "))

    cursor.execute(
        """
        SELECT ProductID
        FROM Inventory
        WHERE ProductID = ?
        """,
        (product_id,)
    )

    item = cursor.fetchone()

    if item is None:

        print("\n❌ Inventory Record Not Found.")

    else:

        quantity = int(input("Enter New Quantity: "))
        reorder_level = int(input("Enter New Reorder Level: "))

        cursor.execute(
            """
            UPDATE Inventory
            SET
                Quantity = ?,
                ReorderLevel = ?
            WHERE ProductID = ?
            """,
            (
                quantity,
                reorder_level,
                product_id
            )
        )

        conn.commit()

        print("\n✅ Inventory Updated Successfully.")

    cursor.close()
    conn.close()


def delete_inventory():

    conn = get_connection()
    cursor = conn.cursor()

    product_id = int(input("Enter Product ID to Delete: "))

    cursor.execute(
        """
        SELECT ProductID
        FROM Inventory
        WHERE ProductID = ?
        """,
        (product_id,)
    )

    item = cursor.fetchone()

    if item is None:

        print("\n❌ Inventory Record Not Found.")

    else:

        cursor.execute(
            """
            DELETE FROM Inventory
            WHERE ProductID = ?
            """,
            (product_id,)
        )

        conn.commit()

        print("\n✅ Inventory Deleted Successfully.")

    cursor.close()
    conn.close()