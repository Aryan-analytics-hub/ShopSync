from services.inventory_crud import (
    view_inventory,
    add_inventory,
    search_inventory,
    update_inventory,
    delete_inventory
)


def inventory_menu():

    while True:

        print("\n========== INVENTORY MENU ==========\n")

        print("1. View Inventory")
        print("2. Add Inventory")
        print("3. Search Inventory")
        print("4. Update Inventory")
        print("5. Delete Inventory")
        print("0. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            view_inventory()

        elif choice == "2":
            add_inventory()

        elif choice == "3":
            search_inventory()

        elif choice == "4":
            update_inventory()

        elif choice == "5":
            delete_inventory()

        elif choice == "0":
            break

        else:
            print("\n❌ Invalid Choice.")