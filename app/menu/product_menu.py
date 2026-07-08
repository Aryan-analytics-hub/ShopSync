from services.product_crud import ( 
    view_products, 
    add_product, 
    search_product, 
    update_product, 
    delete_product
)


def product_menu(): 
    while True: 
        print("\n================PRODUCT MENU===================")
        print("1, View Product: ")
        print("2, Add Product: ")
        print("3, Search Product:")
        print("4, Update Product: ")
        print("5, Delete Product: ")
        print("0, Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1": 
            view_products()
        elif choice == "2": 
            add_product()
        elif choice == "3":
            search_product()
        elif choice == "4": 
            update_product()
        elif choice == "5": 
            delete_product()
        elif choice == "0": 
            print("\n Thanks for using ShopSync.")
            break 
        else:
            print("\nInvalid Choice")


