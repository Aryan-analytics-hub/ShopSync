from database import get_connection


def view_suppliers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            SupplierID,
            SupplierName,
            ContactPerson,
            Email,
            Phone
        FROM Suppliers
        ORDER BY SupplierID
    """)

    suppliers = cursor.fetchall()

    print("\n========== SUPPLIERS ==========\n")

    for supplier in suppliers:

        print(
            f"{supplier.SupplierID} | "
            f"{supplier.SupplierName} | "
            f"{supplier.ContactPerson} | "
            f"{supplier.Email} | "
            f"{supplier.Phone}"
        )

    cursor.close()
    conn.close()


def add_supplier():

    conn = get_connection()
    cursor = conn.cursor()

    supplier_name = input("Enter Supplier Name: ")
    contact_person = input("Enter Contact Person: ")
    phone = input("Enter Phone Number: ")
    email = input("Enter Email: ")
    address = input("Enter Address: ")

    cursor.execute(
        """
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
        )
    )

    conn.commit()

    print("\n✅ Supplier Added Successfully.")

    cursor.close()
    conn.close()


def search_supplier():

    conn = get_connection()
    cursor = conn.cursor()

    supplier_name = input("Enter Supplier Name: ")

    cursor.execute(
        """
        SELECT
            SupplierID,
            SupplierName,
            ContactPerson,
            Email,
            Phone
        FROM Suppliers
        WHERE SupplierName LIKE ?
        """,
        ('%' + supplier_name + '%',)
    )

    suppliers = cursor.fetchall()

    if len(suppliers) == 0:

        print("\nNo Supplier Found.")

    else:

        print("\n========== SEARCH RESULTS ==========\n")

        for supplier in suppliers:

            print(
                f"{supplier.SupplierID} | "
                f"{supplier.SupplierName} | "
                f"{supplier.ContactPerson} | "
                f"{supplier.Email} | "
                f"{supplier.Phone}"
            )

    cursor.close()
    conn.close()


def update_supplier():

    conn = get_connection()
    cursor = conn.cursor()

    supplier_id = int(input("Enter Supplier ID to Update: "))

    cursor.execute(
        """
        SELECT SupplierID
        FROM Suppliers
        WHERE SupplierID = ?
        """,
        (supplier_id,)
    )

    supplier = cursor.fetchone()

    if supplier is None:

        print("\n❌ Supplier Not Found.")

    else:

        supplier_name = input("Enter New Supplier Name: ")
        contact_person = input("Enter New Contact Person: ")
        phone = input("Enter New Phone Number: ")
        email = input("Enter New Email: ")
        address = input("Enter New Address: ")

        cursor.execute(
            """
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
            )
        )

        conn.commit()

        print("\n✅ Supplier Updated Successfully.")

    cursor.close()
    conn.close()


def delete_supplier():

    conn = get_connection()
    cursor = conn.cursor()

    supplier_id = int(input("Enter Supplier ID to Delete: "))

    cursor.execute(
        """
        SELECT SupplierID
        FROM Suppliers
        WHERE SupplierID = ?
        """,
        (supplier_id,)
    )

    supplier = cursor.fetchone()

    if supplier is None:

        print("\n❌ Supplier Not Found.")

    else:

        cursor.execute(
            """
            DELETE FROM Suppliers
            WHERE SupplierID = ?
            """,
            (supplier_id,)
        )

        conn.commit()

        print("\n✅ Supplier Deleted Successfully.")

    cursor.close()
    conn.close()