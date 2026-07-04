CREATE TABLE Orders
(
    OrderID INT IDENTITY(1001,1) PRIMARY KEY,

    CustomerID INT NOT NULL,

    OrderDate DATETIME2 DEFAULT GETDATE(),

    TotalAmount DECIMAL(10,2) NOT NULL
        CHECK (TotalAmount >= 0),

    OrderStatus VARCHAR(20)
        DEFAULT 'Pending'
        CHECK (OrderStatus IN
        (
            'Pending',
            'Confirmed',
            'Packed',
            'Shipped',
            'Delivered',
            'Cancelled'
        )),

    CONSTRAINT FK_Order_Customer
        FOREIGN KEY(CustomerID)
        REFERENCES Customers(CustomerID)
);