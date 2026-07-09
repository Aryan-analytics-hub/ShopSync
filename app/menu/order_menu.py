from services.order_crud import (
    view_orders,
    add_order,
    search_order,
    update_order,
    delete_order
)


def order_menu():

    while True:

        print("\n========== ORDER MENU ==========\n")

        print("1. View Orders")
        print("2. Add Order")
        print("3. Search Order")
        print("4. Update Order Status")
        print("5. Delete Order")
        print("0. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            view_orders()

        elif choice == "2":
            add_order()

        elif choice == "3":
            search_order()

        elif choice == "4":
            update_order()

        elif choice == "5":
            delete_order()

        elif choice == "0":
            break

        else:
            print("\n❌ Invalid Choice.")