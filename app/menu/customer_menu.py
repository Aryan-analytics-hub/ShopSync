from services.customer_crud import (
    view_customers,
    add_customer,
    search_customer,
    update_customer,
    delete_customer
)

def customer_menu():

    while True:

        print("\n========== CUSTOMER MENU ==========\n")

        print("1. View Customers")
        print("2. Add Customer")
        print("3. Search Customer")
        print("4. Update Customer")
        print("5. Delete Customer")
        print("0. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            view_customers()

        elif choice == "2":
            add_customer()

        elif choice == "3":
            search_customer()

        elif choice == "4":
            update_customer()

        elif choice == "5":
            delete_customer()

        elif choice == "0":
            break

        else:
            print("\nInvalid Choice.")