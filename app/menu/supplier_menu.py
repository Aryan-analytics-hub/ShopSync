from services.supplier_crud import (
    view_suppliers,
    add_supplier,
    search_supplier,
    update_supplier,
    delete_supplier
)


def supplier_menu():

    while True:

        print("\n========== SUPPLIER MENU ==========\n")

        print("1. View Suppliers")
        print("2. Add Supplier")
        print("3. Search Supplier")
        print("4. Update Supplier")
        print("5. Delete Supplier")
        print("0. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            view_suppliers()

        elif choice == "2":
            add_supplier()

        elif choice == "3":
            search_supplier()

        elif choice == "4":
            update_supplier()

        elif choice == "5":
            delete_supplier()

        elif choice == "0":
            break

        else:
            print("\nInvalid Choice.")