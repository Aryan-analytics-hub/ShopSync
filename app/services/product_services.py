from faker import Faker
import random

from database import execute_query

fake = Faker("en_IN")


def insert_products(count):

    for _ in range(count):

        product_name = fake.word().title()

        category_id = random.randint(1, 10)

        supplier_id = random.randint(1, 30)

        cost_price = round(random.uniform(100, 5000), 2)

        selling_price = round(
            random.uniform(cost_price, cost_price * 1.5),
            2
        )

        description = fake.sentence()

        execute_query(
            """
            INSERT INTO Products
            (
                ProductName,
                CategoryID,
                SupplierID,
                CostPrice,
                SellingPrice,
                Description
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                product_name,
                category_id,
                supplier_id,
                cost_price,
                selling_price,
                description
            )
        )

        print(f"Inserted : {product_name}")

    print("Products inserted successfully.")