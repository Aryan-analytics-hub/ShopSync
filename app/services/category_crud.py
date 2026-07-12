import pyodbc
from database import get_connection
from utils.display import print_header


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

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        print_header("Add Category")

        category_name = input("Enter Category Name: ").strip()

        if category_name == "":

            print("\n❌ Category Name cannot be empty.")
            return

        if not any(ch.isalpha() for ch in category_name):

            print("\n❌ Category Name must contain at least one alphabet.")
            return

        description = input("Enter Description: ").strip()

        cursor.execute("""
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
        ))

        conn.commit()

        print("\n✅ Category Added Successfully.")

    except pyodbc.IntegrityError:

        print("\n❌ Database Error.")

        print("Possible reasons:")

        print("- Category already exists.")
        print("- Category violates a database constraint.")

    except Exception as e:

        print(f"\n❌ Unexpected Error: {e}")

    finally:

        if cursor:
            cursor.close()

        if conn:
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

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        print_header("Update Category")

        category_id = int(input("Enter Category ID to Update: "))

        cursor.execute("""
            SELECT CategoryID
            FROM Categories
            WHERE CategoryID = ?
        """,
        (category_id,)
        )

        category = cursor.fetchone()

        if category is None:

            print("\n❌ Category Not Found.")
            return

        category_name = input("Enter New Category Name: ").strip()

        if category_name == "":

            print("\n❌ Category Name cannot be empty.")
            return

        if not any(ch.isalpha() for ch in category_name):

            print("\n❌ Category Name must contain at least one alphabet.")
            return

        description = input("Enter New Description: ").strip()

        cursor.execute("""
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
        ))

        conn.commit()

        print("\n✅ Category Updated Successfully.")

    except ValueError:

        print("\n❌ Invalid Category ID.")

    except pyodbc.IntegrityError:

        print("\n❌ Database Error.")

        print("Possible reasons:")

        print("- Category already exists.")
        print("- Category violates a database constraint.")

    except Exception as e:

        print(f"\n❌ Unexpected Error: {e}")

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()



def delete_category():

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        print_header("Delete Category")

        category_id = int(input("Enter Category ID to Delete: "))

        cursor.execute("""
            SELECT CategoryID
            FROM Categories
            WHERE CategoryID = ?
        """,
        (category_id,)
        )

        category = cursor.fetchone()

        if category is None:

            print("\n❌ Category Not Found.")
            return

        cursor.execute("""
            DELETE FROM Categories
            WHERE CategoryID = ?
        """,
        (category_id,)
        )

        conn.commit()

        print("\n✅ Category Deleted Successfully.")

    except ValueError:

        print("\n❌ Invalid Category ID.")

    except pyodbc.IntegrityError:

        print("\n❌ Cannot delete category.")

        print("Possible reasons:")

        print("- Category is assigned to one or more products.")
        print("- Delete or update those products first.")

    except Exception as e:

        print(f"\n❌ Unexpected Error: {e}")

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()