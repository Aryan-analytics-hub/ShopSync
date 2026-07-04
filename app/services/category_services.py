from database import get_connection


def insert_categories():

    categories = [
        ("Electronics", "Electronic gadgets and devices"),
        ("Clothing", "Men and Women clothing"),
        ("Groceries", "Daily grocery products"),
        ("Books", "Books and magazines"),
        ("Furniture", "Home and office furniture"),
        ("Sports", "Sports accessories"),
        ("Beauty", "Beauty and skincare"),
        ("Toys", "Kids toys"),
        ("Footwear", "Shoes and sandals"),
        ("Stationery", "Office and school supplies")
    ]

    conn = get_connection()
    cursor = conn.cursor()

    for category in categories:
        cursor.execute(
            "SELECT COUNT(*) FROM Categories WHERE CategoryName = ?",
            category[0]
        )

        exists = cursor.fetchone()[0]

        if exists == 0:
            cursor.execute("""
                INSERT INTO Categories
                (CategoryName, Description)
                VALUES (?, ?)
            """, category)

            print(f"Inserted: {category[0]}")

        else:
            print(f"Skipped: {category[0]} (already exists)")

    conn.commit()
    conn.close()
    print("✅ Categories processed successfully.")