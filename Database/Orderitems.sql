CREATE TABLE OrderItems
(
    OrderItemID INT IDENTITY(1,1) PRIMARY KEY,

    OrderID INT NOT NULL,

    ProductID INT NOT NULL,

    Quantity INT NOT NULL
        CHECK (Quantity > 0),

    UnitPrice DECIMAL(10,2) NOT NULL
        CHECK (UnitPrice >= 0),

    SubTotal AS (Quantity * UnitPrice),

    CONSTRAINT FK_OrderItem_Order
        FOREIGN KEY(OrderID)
        REFERENCES Orders(OrderID),

    CONSTRAINT FK_OrderItem_Product
        FOREIGN KEY(ProductID)
        REFERENCES Products(ProductID)
);