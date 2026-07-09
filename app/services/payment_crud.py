from database import get_connection


def view_payments():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            PaymentID,
            OrderID,
            PaymentDate,
            PaymentMethod,
            Amount,
            PaymentStatus,
            TransactionReference
        FROM Payments
        ORDER BY PaymentID
    """)

    payments = cursor.fetchall()

    print("\n========== PAYMENTS ==========\n")

    for payment in payments:

        print(
            f"{payment.PaymentID} | "
            f"Order ID: {payment.OrderID} | "
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
            OrderID
        FROM Orders
        ORDER BY OrderID
    """)

    orders = cursor.fetchall()

    for order in orders:

        print(order.OrderID)

    print()

    order_id = int(input("Enter Order ID: "))

    print("\nPayment Methods")
    print("Cash")
    print("Card")
    print("UPI")
    print("Net Banking")

    payment_method = input("\nEnter Payment Method: ")

    amount = float(input("Enter Amount: "))

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


def search_payment():

    conn = get_connection()
    cursor = conn.cursor()

    payment_id = int(input("Enter Payment ID: "))

    cursor.execute("""
        SELECT
            PaymentID,
            OrderID,
            PaymentDate,
            PaymentMethod,
            Amount,
            PaymentStatus,
            TransactionReference
        FROM Payments
        WHERE PaymentID = ?
    """,
    (payment_id,)
    )

    payment = cursor.fetchone()

    if payment is None:

        print("\n❌ Payment Not Found.")

    else:

        print("\n========== PAYMENT ==========\n")

        print(
            f"{payment.PaymentID} | "
            f"Order ID: {payment.OrderID} | "
            f"{payment.PaymentDate} | "
            f"{payment.PaymentMethod} | "
            f"₹{payment.Amount} | "
            f"{payment.PaymentStatus} | "
            f"{payment.TransactionReference}"
        )

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