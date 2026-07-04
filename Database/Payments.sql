CREATE TABLE Payments
(
    PaymentID INT IDENTITY(1,1) PRIMARY KEY,

    OrderID INT NOT NULL,

    PaymentDate DATETIME2 DEFAULT GETDATE(),

    PaymentMethod VARCHAR(20)
        CHECK (PaymentMethod IN
        (
            'Cash',
            'Card',
            'UPI',
            'Net Banking'
        )),

    Amount DECIMAL(10,2) NOT NULL
        CHECK (Amount >= 0),

    PaymentStatus VARCHAR(20)
        DEFAULT 'Pending'
        CHECK (PaymentStatus IN
        (
            'Pending',
            'Completed',
            'Failed',
            'Refunded'
        )),

    TransactionReference VARCHAR(100) UNIQUE,

    CONSTRAINT FK_Payment_Order
        FOREIGN KEY(OrderID)
        REFERENCES Orders(OrderID)
);