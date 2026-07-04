from faker import Faker
from database import get_connection

fake = Faker("en_IN")


def insert_suppliers():

    conn = get_connection()
    cursor = conn.cursor()

    for _ in range(30):

        supplier_name = fake.company()
        contact_person = fake.name()
        phone = fake.phone_number()
        email = fake.company_email()
        address = fake.address()

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
    conn.close()

    print("✅ Suppliers inserted successfully.")