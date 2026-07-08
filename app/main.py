from menu.product_menu import product_menu
from menu.customer_menu import customer_menu
from menu.supplier_menu import supplier_menu
from menu.category_menu import category_menu


def main():

    while True:

        print("\n========== SHOPSYNC ==========\n")

        print("1. Product Management")
        print("2. Customer Management")
        print("3. Supplier Management")
        print("4. Category Management")
        print("5. Inventory Management")
        print("6. Order Management")
        print("7. Payment Management")
        print("8. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            product_menu()

        elif choice == "2":
            customer_menu()

        elif choice == "3":
            supplier_menu()

        elif choice == "4":
            category_menu()

        elif choice == "5":
            print("\nInventory Module Coming Soon...")

        elif choice == "6":
            print("\nOrder Module Coming Soon...")

        elif choice == "7":
            print("\nPayment Module Coming soon.....")
        
        elif choice == "8":
            print("\nThanks for using ShopSync")
            break

        else:
            print("\nInvalid Choice!")


main()