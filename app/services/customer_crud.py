import pyodbc
from database import get_connection
from utils.display import print_header

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


import pyodbc

def add_customer():

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        print_header("Add Customer")

        first_name = input("Enter First Name: ").strip()

        if not first_name.replace(" ", "").isalpha():

            print("\n❌ First Name should contain only letters.")
            return

        last_name = input("Enter Last Name: ").strip()

        if not last_name.replace(" ", "").isalpha():

            print("\n❌ Last Name should contain only letters.")
            return

        email = input("Enter Email: ").strip()

        if "@" not in email or "." not in email:

            print("\n❌ Invalid Email Address.")
            return

        phone = input("Enter Phone Number: ").strip()

        if not phone.isdigit():

            print("\n❌ Phone Number should contain only digits.")
            return

        if len(phone) != 10:

            print("\n❌ Phone Number must be exactly 10 digits.")
            return

        address = input("Enter Address: ").strip()

        city = input("Enter City: ").strip()

        if not city.replace(" ", "").isalpha():

            print("\n❌ City should contain only letters.")
            return

        state = input("Enter State: ").strip()

        if not state.replace(" ", "").isalpha():

            print("\n❌ State should contain only letters.")
            return

        postal_code = input("Enter Postal Code: ").strip()

        if not postal_code.isdigit():

            print("\n❌ Postal Code should contain only digits.")
            return

        if len(postal_code) != 6:

            print("\n❌ Postal Code must be exactly 6 digits.")
            return

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

    except pyodbc.IntegrityError:

        print("\n❌ Database Error.")

        print("Possible reasons:")

        print("- Email already exists.")
        print("- Customer violates a database constraint.")

    except Exception as e:

        print(f"\n❌ Unexpected Error: {e}")

    finally:

        if cursor:
            cursor.close()

        if conn:
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

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        print_header("Update Customer")

        customer_id = int(input("Enter Customer ID to Update: "))

        cursor.execute("""
            SELECT CustomerID
            FROM Customers
            WHERE CustomerID = ?
        """,
        (customer_id,)
        )

        customer = cursor.fetchone()

        if customer is None:

            print("\n❌ Customer Not Found.")
            return

        first_name = input("Enter New First Name: ").strip()

        if not first_name.replace(" ", "").isalpha():

            print("\n❌ First Name should contain only letters.")
            return

        last_name = input("Enter New Last Name: ").strip()

        if not last_name.replace(" ", "").isalpha():

            print("\n❌ Last Name should contain only letters.")
            return

        email = input("Enter New Email: ").strip()

        if "@" not in email or "." not in email:

            print("\n❌ Invalid Email Address.")
            return

        phone = input("Enter New Phone Number: ").strip()

        if not phone.isdigit():

            print("\n❌ Phone Number should contain only digits.")
            return

        if len(phone) != 10:

            print("\n❌ Phone Number must be exactly 10 digits.")
            return

        address = input("Enter New Address: ").strip()

        city = input("Enter New City: ").strip()

        if not city.replace(" ", "").isalpha():

            print("\n❌ City should contain only letters.")
            return

        state = input("Enter New State: ").strip()

        if not state.replace(" ", "").isalpha():

            print("\n❌ State should contain only letters.")
            return

        postal_code = input("Enter New Postal Code: ").strip()

        if not postal_code.isdigit():

            print("\n❌ Postal Code should contain only digits.")
            return

        if len(postal_code) != 6:

            print("\n❌ Postal Code must be exactly 6 digits.")
            return

        cursor.execute("""
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
        ))

        conn.commit()

        print("\n✅ Customer Updated Successfully.")

    except ValueError:

        print("\n❌ Invalid Customer ID.")

    except pyodbc.IntegrityError:

        print("\n❌ Database Error.")

        print("Possible reasons:")

        print("- Email already exists.")
        print("- Customer data violates a database constraint.")

    except Exception as e:

        print(f"\n❌ Unexpected Error: {e}")

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


def delete_customer():

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        print_header("Delete Customer")

        customer_id = int(input("Enter Customer ID to Delete: "))

        cursor.execute("""
            SELECT CustomerID
            FROM Customers
            WHERE CustomerID = ?
        """,
        (customer_id,)
        )

        customer = cursor.fetchone()

        if customer is None:

            print("\n❌ Customer Not Found.")
            return

        cursor.execute("""
            DELETE FROM Customers
            WHERE CustomerID = ?
        """,
        (customer_id,)
        )

        conn.commit()

        print("\n✅ Customer Deleted Successfully.")

    except ValueError:

        print("\n❌ Invalid Customer ID.")

    except pyodbc.IntegrityError:

        print("\n❌ Cannot delete customer.")

        print("Possible reasons:")
        print("- Customer has existing orders.")
        print("- Delete the customer's orders first.")

    except Exception as e:

        print(f"\n❌ Unexpected Error: {e}")

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()