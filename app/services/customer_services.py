from faker import Faker
from database import execute_query, fetch_one

fake = Faker("en_IN")


def insert_customers(count):

    for _ in range(count):

        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.unique.email()
        phone = fake.phone_number()
        address = fake.street_address()
        city = fake.city()
        state = fake.state()
        postal_code = fake.postcode()

        exists = fetch_one(
            "SELECT COUNT(*) FROM Customers WHERE Email = ?",
            (email,)
        )[0]

        if exists == 0:

            execute_query(
                """
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
                )
            )

            print(f"Inserted: {first_name} {last_name}")

        else:

            print(f"Skipped: {email}")

    print("Customers inserted successfully.")