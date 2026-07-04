from services.category_services import insert_categories
from services.supplier_services import insert_suppliers
from services.customer_services import insert_customers
from services.product_services import insert_products
from services.inventory_services import insert_inventory
from services.order_services import insert_orders
from services.orderitem_services import insert_order_items 
from services.payment_services import insert_payments


insert_categories()
insert_suppliers()
insert_customers(50)
insert_products(100)
insert_inventory()
insert_orders(300)
insert_order_items(900)
insert_payments(300)