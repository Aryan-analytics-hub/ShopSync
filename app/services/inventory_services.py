from database import get_connection
import random


def insert_inventory():

    inventory_data = []

    for product_id in range(1, 101):

        quantity = random.randint(0, 250)
        reorder_level = random.randint(10, 50)

        inventory_data.append(
            (
                product_id,
                quantity,
                reorder_level
            )
        )

    conn = get_connection()
    cursor = conn.cursor()

    for inventory in inventory_data:

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM Inventory
            WHERE ProductID = ?
            """,
            inventory[0]
        )

        exists = cursor.fetchone()[0]

        if exists == 0:

            cursor.execute(
                """
                INSERT INTO Inventory
                (
                    ProductID,
                    Quantity,
                    ReorderLevel
                )
                VALUES
                (
                    ?, ?, ?
                )
                """,
                inventory
            )

            print(f"Inserted ProductID : {inventory[0]}")

        else:

            print(f"Skipped ProductID : {inventory[0]}")

    conn.commit()
    cursor.close()
    conn.close()

    print("Inventory inserted successfully.")