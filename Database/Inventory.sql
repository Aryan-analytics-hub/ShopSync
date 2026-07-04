CREATE TABLE Inventory
(
    InventoryID INT IDENTITY(1,1) PRIMARY KEY,

    ProductID INT NOT NULL UNIQUE,

    Quantity INT NOT NULL DEFAULT 0
        CHECK (Quantity >= 0),

    ReorderLevel INT NOT NULL DEFAULT 10
        CHECK (ReorderLevel >= 0),

    LastUpdated DATETIME2 DEFAULT GETDATE(),

    CONSTRAINT FK_Inventory_Product
        FOREIGN KEY(ProductID)
        REFERENCES Products(ProductID)
);