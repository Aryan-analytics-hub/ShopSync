import pyodbc


def handle_database_error(error):

    error_message = str(error)

    if isinstance(error, ValueError):

        print("\n❌ Invalid input.")
        print("Please enter the correct data type.")

    elif isinstance(error, pyodbc.IntegrityError):

        if "FK_Product_Supplier" in error_message:

            print("\n❌ Supplier ID does not exist.")

        elif "FK_Product_Category" in error_message:

            print("\n❌ Category ID does not exist.")

        elif "FK_Order_Customer" in error_message:

            print("\n❌ Customer ID does not exist.")

        elif "FK_OrderItem_Order" in error_message:

            print("\n❌ Order ID does not exist.")

        elif "FK_OrderItem_Product" in error_message:

            print("\n❌ Product ID does not exist.")

        elif "FK_Payment_Order" in error_message:

            print("\n❌ Order ID does not exist.")

        elif "CHECK" in error_message:

            print("\n❌ Invalid value entered.")

        elif "UNIQUE" in error_message:

            print("\n❌ Duplicate value already exists.")

        else:

            print("\n❌ Database constraint violated.")

    else:

        print(f"\n❌ Unexpected Error:\n{error}")