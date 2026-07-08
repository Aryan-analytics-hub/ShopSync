from database import get_connection


def view_customers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            CustomerID,
            FirstName,
            LastName,
            Email,
            Phone
        FROM Customers
        ORDER BY CustomerID
    """)

    customers = cursor.fetchall()

    print("\n========== CUSTOMERS ==========\n")

    for customer in customers:

        print(
            f"{customer.CustomerID} | "
            f"{customer.FirstName} {customer.LastName} | "
            f"{customer.Email} | "
            f"{customer.Phone}"
        )

    cursor.close()
    conn.close()


def add_customer():

    conn = get_connection()
    cursor = conn.cursor()

    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    email = input("Enter Email: ")
    phone = input("Enter Phone Number: ")
    address = input("Enter Address: ")
    city = input("Enter City: ")
    state = input("Enter State: ")
    postal_code = input("Enter Postal Code: ")

    cursor.execute("""
        INSERT INTO Customers
        (
            FirstName,
            LastName,
            Email,
            Phone,
            Address,
            City,
            State,
            PostalCode
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        first_name,
        last_name,
        email,
        phone,
        address,
        city,
        state,
        postal_code
    ))

    conn.commit()

    print("\n✅ Customer Added Successfully.")

    cursor.close()
    conn.close()


def search_customer():

    conn = get_connection()
    cursor = conn.cursor()

    first_name = input("Enter First Name: ")

    cursor.execute(
        """
        SELECT
            CustomerID,
            FirstName,
            LastName,
            Email,
            Phone
        FROM Customers
        WHERE FirstName LIKE ?
        """,
        ('%' + first_name + '%',)
    )

    customers = cursor.fetchall()

    if len(customers) == 0:

        print("\nNo Customer Found.")

    else:

        print("\n========== SEARCH RESULTS ==========\n")

        for customer in customers:

            print(
                f"{customer.CustomerID} | "
                f"{customer.FirstName} {customer.LastName} | "
                f"{customer.Email} | "
                f"{customer.Phone}"
            )

    cursor.close()
    conn.close()


def update_customer():

    conn = get_connection()
    cursor = conn.cursor()

    customer_id = int(input("Enter Customer ID to Update: "))

    cursor.execute(
        """
        SELECT CustomerID
        FROM Customers
        WHERE CustomerID = ?
        """,
        (customer_id,)
    )

    customer = cursor.fetchone()

    if customer is None:

        print("\n❌ Customer Not Found.")

    else:

        first_name = input("Enter New First Name: ")
        last_name = input("Enter New Last Name: ")
        email = input("Enter New Email: ")
        phone = input("Enter New Phone Number: ")
        address = input("Enter New Address: ")
        city = input("Enter New City: ")
        state = input("Enter New State: ")
        postal_code = input("Enter New Postal Code: ")

        cursor.execute(
            """
            UPDATE Customers
            SET
                FirstName = ?,
                LastName = ?,
                Email = ?,
                Phone = ?,
                Address = ?,
                City = ?,
                State = ?,
                PostalCode = ?
            WHERE CustomerID = ?
            """,
            (
                first_name,
                last_name,
                email,
                phone,
                address,
                city,
                state,
                postal_code,
                customer_id
            )
        )

        conn.commit()

        print("\n✅ Customer Updated Successfully.")

    cursor.close()
    conn.close()


def delete_customer():

    conn = get_connection()
    cursor = conn.cursor()

    customer_id = int(input("Enter Customer ID to Delete: "))

    cursor.execute(
        """
        SELECT CustomerID
        FROM Customers
        WHERE CustomerID = ?
        """,
        (customer_id,)
    )

    customer = cursor.fetchone()

    if customer is None:

        print("\n❌ Customer Not Found.")

    else:

        cursor.execute(
            """
            DELETE FROM Customers
            WHERE CustomerID = ?
            """,
            (customer_id,)
        )

        conn.commit()

        print("\n✅ Customer Deleted Successfully.")

    cursor.close()
    conn.close()

