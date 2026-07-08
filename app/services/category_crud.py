from database import get_connection


def view_categories():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            CategoryID,
            CategoryName,
            Description
        FROM Categories
        ORDER BY CategoryID
    """)

    categories = cursor.fetchall()

    print("\n========== CATEGORIES ==========\n")

    for category in categories:

        print(
            f"{category.CategoryID} | "
            f"{category.CategoryName} | "
            f"{category.Description}"
        )

    cursor.close()
    conn.close()


def add_category():

    conn = get_connection()
    cursor = conn.cursor()

    category_name = input("Enter Category Name: ")
    description = input("Enter Description: ")

    cursor.execute(
        """
        INSERT INTO Categories
        (
            CategoryName,
            Description
        )
        VALUES (?, ?)
        """,
        (
            category_name,
            description
        )
    )

    conn.commit()

    print("\n✅ Category Added Successfully.")

    cursor.close()
    conn.close()


def search_category():

    conn = get_connection()
    cursor = conn.cursor()

    category_name = input("Enter Category Name: ")

    cursor.execute(
        """
        SELECT
            CategoryID,
            CategoryName,
            Description
        FROM Categories
        WHERE CategoryName LIKE ?
        """,
        ('%' + category_name + '%',)
    )

    categories = cursor.fetchall()

    if len(categories) == 0:

        print("\nNo Category Found.")

    else:

        print("\n========== SEARCH RESULTS ==========\n")

        for category in categories:

            print(
                f"{category.CategoryID} | "
                f"{category.CategoryName} | "
                f"{category.Description}"
            )

    cursor.close()
    conn.close()


def update_category():

    conn = get_connection()
    cursor = conn.cursor()

    category_id = int(input("Enter Category ID to Update: "))

    cursor.execute(
        """
        SELECT CategoryID
        FROM Categories
        WHERE CategoryID = ?
        """,
        (category_id,)
    )

    category = cursor.fetchone()

    if category is None:

        print("\n❌ Category Not Found.")

    else:

        category_name = input("Enter New Category Name: ")
        description = input("Enter New Description: ")

        cursor.execute(
            """
            UPDATE Categories
            SET
                CategoryName = ?,
                Description = ?
            WHERE CategoryID = ?
            """,
            (
                category_name,
                description,
                category_id
            )
        )

        conn.commit()

        print("\n✅ Category Updated Successfully.")

    cursor.close()
    conn.close()


def delete_category():

    conn = get_connection()
    cursor = conn.cursor()

    category_id = int(input("Enter Category ID to Delete: "))

    cursor.execute(
        """
        SELECT CategoryID
        FROM Categories
        WHERE CategoryID = ?
        """,
        (category_id,)
    )

    category = cursor.fetchone()

    if category is None:

        print("\n❌ Category Not Found.")

    else:

        cursor.execute(
            """
            DELETE FROM Categories
            WHERE CategoryID = ?
            """,
            (category_id,)
        )

        conn.commit()

        print("\n✅ Category Deleted Successfully.")

    cursor.close()
    conn.close()