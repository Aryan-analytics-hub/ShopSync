from services.category_crud import (
    view_categories,
    add_category,
    search_category,
    update_category,
    delete_category
)


def category_menu():

    while True:

        print("\n========== CATEGORY MENU ==========\n")

        print("1. View Categories")
        print("2. Add Category")
        print("3. Search Category")
        print("4. Update Category")
        print("5. Delete Category")
        print("0. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            view_categories()

        elif choice == "2":
            add_category()

        elif choice == "3":
            search_category()

        elif choice == "4":
            update_category()

        elif choice == "5":
            delete_category()

        elif choice == "0":
            break

        else:
            print("\n❌ Invalid Choice.")