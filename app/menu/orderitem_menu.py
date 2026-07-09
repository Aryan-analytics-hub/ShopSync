from services.orderitem_crud import (
    view_order_items,
    add_order_item,
    search_order_item,
    update_order_item,
    delete_order_item
)


def orderitem_menu():

    while True:

        print("\n========== ORDER ITEM MENU ==========\n")

        print("1. View Order Items")
        print("2. Add Order Item")
        print("3. Search Order Item")
        print("4. Update Order Item")
        print("5. Delete Order Item")
        print("0. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            view_order_items()

        elif choice == "2":
            add_order_item()

        elif choice == "3":
            search_order_item()

        elif choice == "4":
            update_order_item()

        elif choice == "5":
            delete_order_item()

        elif choice == "0":
            break

        else:
            print("\n❌ Invalid Choice.")