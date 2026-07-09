from services.payment_crud import (
    view_payments,
    add_payment,
    search_payment,
    update_payment,
    delete_payment
)


def payment_menu():

    while True:

        print("\n========== PAYMENT MENU ==========\n")

        print("1. View Payments")
        print("2. Add Payment")
        print("3. Search Payment")
        print("4. Update Payment")
        print("5. Delete Payment")
        print("0. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            view_payments()

        elif choice == "2":
            add_payment()

        elif choice == "3":
            search_payment()

        elif choice == "4":
            update_payment()

        elif choice == "5":
            delete_payment()

        elif choice == "0":
            break

        else:
            print("\n❌ Invalid Choice.")