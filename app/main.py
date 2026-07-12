from dashboard.dashboard import dashboard
from menu.product_menu import product_menu
from menu.customer_menu import customer_menu
from menu.supplier_menu import supplier_menu
from menu.category_menu import category_menu
from menu.inventory_menu import inventory_menu
from menu.order_menu import order_menu
from menu.orderitem_menu import orderitem_menu
from menu.payment_menu import payment_menu
from menu.report_menu import report_menu


def main():

    while True:

        print("\n========== SHOPSYNC ==========\n")

        print("1. Product Management")
        print("2. Customer Management")
        print("3. Supplier Management")
        print("4. Category Management")
        print("5. Inventory Management")
        print("6. Order Management")
        print("7. OrderItem Management")
        print("8. Payment Management")
        print("9, Report")
        print("10, Dashboard")
        print("0, Exit")

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
            inventory_menu()

        elif choice == "6":
            order_menu()

        elif choice == "7":
            orderitem_menu()
        
        elif choice == "8":
            payment_menu()

        elif choice == "9":
            report_menu()
        
        elif choice == "10":
            dashboard()
            
        elif choice == "0":
            print("\nThanks for Using ShopSync")
        
        else:
            print("\nInvalid Choice!")


main()