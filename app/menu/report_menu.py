from reports.sales_report import sales_report
from reports.inventory_report import inventory_report
from reports.product_report import product_report
from reports.payment_report import payment_report
from reports.customer_report import customer_report
from reports.supplier_report import supplier_report


def report_menu():

    while True:

        print("\n========== REPORT MENU ==========")

        print("1. Sales Report")
        print("2. Inventory Report")
        print("3. Product Report")
        print("4. Payment Report")
        print("5. Customer Report")
        print("6. Supplier Report")
        print("0. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            sales_report()

        elif choice == "2":

            inventory_report()

        elif choice == "3":

            product_report()

        elif choice == "4":

            payment_report()

        elif choice == "5":

            customer_report()

        elif choice == "6":

            supplier_report()

        elif choice == "0":

            break

        else:

            print("\n❌ Invalid Choice.")