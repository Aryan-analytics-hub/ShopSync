import pyodbc
from database import get_connection
from utils.display import print_header


def view_suppliers():

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                SupplierID,
                SupplierName,
                ContactPerson,
                Phone,
                Email,
                Address
            FROM Suppliers
            ORDER BY SupplierID
        """)

        suppliers = cursor.fetchall()

        print_header("Suppliers")
        print("ID | Supplier | Contact Person | Phone | Email | Address")
        print("-" * 120)

        for supplier in suppliers:

            print(
                f"{supplier.SupplierID} | "
                f"{supplier.SupplierName} | "
                f"{supplier.ContactPerson} | "
                f"{supplier.Phone} | "
                f"{supplier.Email} | "
                f"{supplier.Address}"
            )

    except Exception as e:

        print(f"\n❌ Unexpected Error: {e}")

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

def add_supplier():

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        print_header("Add Supplier")

        supplier_name = input("Enter Supplier Name: ").strip()

        if not supplier_name.replace(" ", "").isalpha():

            print("\n❌ Supplier Name should contain only letters.")
            return

        contact_person = input("Enter Contact Person: ").strip()

        if not contact_person.replace(" ", "").isalpha():

            print("\n❌ Contact Person should contain only letters.")
            return

        phone = input("Enter Phone Number: ").strip()

        if not phone.isdigit():

            print("\n❌ Phone Number should contain only digits.")
            return

        if len(phone) != 10:

            print("\n❌ Phone Number must be exactly 10 digits.")
            return

        email = input("Enter Email: ").strip()

        if "@" not in email or "." not in email:

            print("\n❌ Invalid Email Address.")
            return

        address = input("Enter Address: ").strip()

        cursor.execute("""
            INSERT INTO Suppliers
            (
                SupplierName,
                ContactPerson,
                Phone,
                Email,
                Address
            )
            VALUES (?, ?, ?, ?, ?)
        """,
        (
            supplier_name,
            contact_person,
            phone,
            email,
            address
        ))

        conn.commit()

        print("\n✅ Supplier Added Successfully.")

    except pyodbc.IntegrityError:

        print("\n❌ Database Error.")

        print("Possible reasons:")

        print("- Supplier already exists.")
        print("- Email violates a database constraint.")

    except Exception as e:

        print(f"\n❌ Unexpected Error: {e}")

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


def search_supplier():

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        print_header("Search Supplier")

        supplier_name = input("Enter Supplier Name: ").strip()

        cursor.execute("""
            SELECT
                SupplierID,
                SupplierName,
                ContactPerson,
                Phone,
                Email,
                Address
            FROM Suppliers
            WHERE SupplierName LIKE ?
            ORDER BY SupplierName
        """,
        ('%' + supplier_name + '%',)
        )

        suppliers = cursor.fetchall()

        if len(suppliers) == 0:

            print("\n❌ Supplier Not Found.")

        else:

            print("\nID | Supplier | Contact Person | Phone | Email | Address")
            print("-" * 120)

            for supplier in suppliers:

                print(
                    f"{supplier.SupplierID} | "
                    f"{supplier.SupplierName} | "
                    f"{supplier.ContactPerson} | "
                    f"{supplier.Phone} | "
                    f"{supplier.Email} | "
                    f"{supplier.Address}"
                )

    except Exception as e:

        print(f"\n❌ Unexpected Error: {e}")

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


def update_supplier():

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        print_header("Update Supplier")

        supplier_id = int(input("Enter Supplier ID to Update: "))

        cursor.execute("""
            SELECT SupplierID
            FROM Suppliers
            WHERE SupplierID = ?
        """,
        (supplier_id,)
        )

        supplier = cursor.fetchone()

        if supplier is None:

            print("\n❌ Supplier Not Found.")
            return

        supplier_name = input("Enter New Supplier Name: ").strip()

        if not supplier_name.replace(" ", "").isalpha():

            print("\n❌ Supplier Name should contain only letters.")
            return

        contact_person = input("Enter New Contact Person: ").strip()

        if not contact_person.replace(" ", "").isalpha():

            print("\n❌ Contact Person should contain only letters.")
            return

        phone = input("Enter New Phone Number: ").strip()

        if not phone.isdigit():

            print("\n❌ Phone Number should contain only digits.")
            return

        if len(phone) != 10:

            print("\n❌ Phone Number must be exactly 10 digits.")
            return

        email = input("Enter New Email: ").strip()

        if "@" not in email or "." not in email:

            print("\n❌ Invalid Email Address.")
            return

        address = input("Enter New Address: ").strip()

        cursor.execute("""
            UPDATE Suppliers
            SET
                SupplierName = ?,
                ContactPerson = ?,
                Phone = ?,
                Email = ?,
                Address = ?
            WHERE SupplierID = ?
        """,
        (
            supplier_name,
            contact_person,
            phone,
            email,
            address,
            supplier_id
        ))

        conn.commit()

        print("\n✅ Supplier Updated Successfully.")

    except ValueError:

        print("\n❌ Invalid Supplier ID.")

    except pyodbc.IntegrityError:

        print("\n❌ Database Error.")

        print("Possible reasons:")

        print("- Email already exists.")
        print("- Supplier data violates a database constraint.")

    except Exception as e:

        print(f"\n❌ Unexpected Error: {e}")

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

def delete_supplier():

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        print_header("Delete Supplier")

        supplier_id = int(input("Enter Supplier ID to Delete: "))

        cursor.execute("""
            SELECT SupplierID
            FROM Suppliers
            WHERE SupplierID = ?
        """,
        (supplier_id,)
        )

        supplier = cursor.fetchone()

        if supplier is None:

            print("\n❌ Supplier Not Found.")
            return

        cursor.execute("""
            DELETE FROM Suppliers
            WHERE SupplierID = ?
        """,
        (supplier_id,)
        )

        conn.commit()

        print("\n✅ Supplier Deleted Successfully.")

    except ValueError:

        print("\n❌ Invalid Supplier ID.")

    except pyodbc.IntegrityError:

        print("\n❌ Cannot delete supplier.")

        print("Possible reasons:")

        print("- Supplier is linked to one or more products.")
        print("- Delete or update those products first.")

    except Exception as e:

        print(f"\n❌ Unexpected Error: {e}")

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()