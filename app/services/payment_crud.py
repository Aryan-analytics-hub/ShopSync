from database import get_connection
from utils.display import print_header


def view_payments():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            P.PaymentID,

            P.OrderID,

            C.FirstName,

            C.LastName,

            P.PaymentDate,

            P.PaymentMethod,

            P.Amount,

            P.PaymentStatus,

            P.TransactionReference

        FROM Payments AS P

        INNER JOIN Orders AS O
            ON P.OrderID = O.OrderID

        INNER JOIN Customers AS C
            ON O.CustomerID = C.CustomerID

        ORDER BY P.PaymentID""")

    payments = cursor.fetchall()

    print_header("\nPAYMENTS\n")
    print("ID | Order | Customer | Method | Amount | Status")
    print("-" * 100)    


    for payment in payments:

        print(
            f"{payment.PaymentID} | "
            f"Order: {payment.OrderID} | "
            f"{payment.FirstName} {payment.LastName} | "
            f"{payment.PaymentDate} | "
            f"{payment.PaymentMethod} | "
            f"₹{payment.Amount} | "
            f"{payment.PaymentStatus} | "
            f"{payment.TransactionReference}"
        )

    cursor.close()
    conn.close()


def add_payment():

    conn = get_connection()
    cursor = conn.cursor()

    print("\n========== AVAILABLE ORDERS ==========\n")

    cursor.execute("""
        SELECT
            OrderID,
            TotalAmount
        FROM Orders
        ORDER BY OrderID
    """)

    orders = cursor.fetchall()

    for order in orders:

        print(
            f"{order.OrderID} | "
            f"Total Amount : ₹{order.TotalAmount}"
        )

    print()

    order_id = int(input("Enter Order ID: "))

    # Check whether Order exists

    cursor.execute("""
        SELECT
            TotalAmount
        FROM Orders
        WHERE OrderID = ?
    """,
    (order_id,)
    )

    order = cursor.fetchone()

    if order is None:

        print("\n❌ Order Not Found.")

        cursor.close()
        conn.close()

        return

    order_total = order.TotalAmount

    print("\nPayment Methods")
    print("Cash")
    print("Card")
    print("UPI")
    print("Net Banking")

    payment_method = input("\nEnter Payment Method: ")

    amount = float(input("Enter Amount: "))

    # Validation 1

    if amount <= 0:

        print("\n❌ Payment amount must be greater than zero.")

        cursor.close()
        conn.close()

        return

    # Validation 2

    if amount > order_total:

        print("\n❌ Payment exceeds Order Total.")

        print(f"Order Total : ₹{order_total}")

        cursor.close()
        conn.close()

        return

    print("\nPayment Status")
    print("Pending")
    print("Completed")
    print("Failed")
    print("Refunded")

    payment_status = input("\nEnter Payment Status: ")

    transaction_reference = input("Enter Transaction Reference: ")

    cursor.execute("""
        INSERT INTO Payments
        (
            OrderID,
            PaymentMethod,
            Amount,
            PaymentStatus,
            TransactionReference
        )
        VALUES (?, ?, ?, ?, ?)
    """,
    (
        order_id,
        payment_method,
        amount,
        payment_status,
        transaction_reference
    ))

    conn.commit()

    print("\n✅ Payment Added Successfully.")

    cursor.close()
    conn.close()
# -------------------------------------------------------------
def search_payment():

    conn = get_connection()
    cursor = conn.cursor()

    payment_id = int(input("Enter Payment ID: "))

    cursor.execute("""
        SELECT

            P.PaymentID,

            P.OrderID,

            C.FirstName,

            C.LastName,

            P.PaymentDate,

            P.PaymentMethod,

            P.Amount,

            P.PaymentStatus,

            P.TransactionReference

        FROM Payments AS P

        INNER JOIN Orders AS O
            ON P.OrderID = O.OrderID

        INNER JOIN Customers AS C
            ON O.CustomerID = C.CustomerID

        WHERE P.PaymentID = ?
    """,
    (payment_id,)
    )

    payment = cursor.fetchone()

    if payment is None:

        print("\n❌ Payment Not Found.")

    else:

        print_header("Payment")

        print(f"Payment ID : {payment.PaymentID}")
        print(f"Order ID   : {payment.OrderID}")
        print(f"Customer   : {payment.FirstName} {payment.LastName}")
        print(f"Date       : {payment.PaymentDate}")
        print(f"Method     : {payment.PaymentMethod}")
        print(f"Amount     : ₹{payment.Amount}")
        print(f"Status     : {payment.PaymentStatus}")
        print(f"Reference  : {payment.TransactionReference}")

    cursor.close()
    conn.close()

def update_payment():

    conn = get_connection()
    cursor = conn.cursor()

    payment_id = int(input("Enter Payment ID: "))

    cursor.execute("""
        SELECT PaymentID
        FROM Payments
        WHERE PaymentID = ?
    """,
    (payment_id,)
    )

    payment = cursor.fetchone()

    if payment is None:

        print("\n❌ Payment Not Found.")

    else:

        print("\nPayment Status")
        print("Pending")
        print("Completed")
        print("Failed")
        print("Refunded")

        payment_status = input("\nEnter New Payment Status: ")

        cursor.execute("""
            UPDATE Payments
            SET PaymentStatus = ?
            WHERE PaymentID = ?
        """,
        (
            payment_status,
            payment_id
        ))

        conn.commit()

        print("\n✅ Payment Updated Successfully.")

    cursor.close()
    conn.close()


def delete_payment():

    conn = get_connection()
    cursor = conn.cursor()

    payment_id = int(input("Enter Payment ID: "))

    cursor.execute("""
        SELECT PaymentID
        FROM Payments
        WHERE PaymentID = ?
    """,
    (payment_id,)
    )

    payment = cursor.fetchone()

    if payment is None:

        print("\n❌ Payment Not Found.")

    else:

        cursor.execute("""
            DELETE FROM Payments
            WHERE PaymentID = ?
        """,
        (payment_id,)
        )

        conn.commit()

        print("\n✅ Payment Deleted Successfully.")

    cursor.close()
    conn.close()