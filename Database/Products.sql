CREATE TABLE Products
(
    ProductID INT IDENTITY(1,1) PRIMARY KEY,

    ProductName VARCHAR(150) NOT NULL,

    CategoryID INT NOT NULL,

    SupplierID INT NOT NULL,

    CostPrice DECIMAL(10,2) NOT NULL
        CHECK (CostPrice >= 0),

    SellingPrice DECIMAL(10,2) NOT NULL
        CHECK (SellingPrice >= CostPrice),

    Description VARCHAR(255),

    CreatedAt DATETIME2 DEFAULT GETDATE(),

    CONSTRAINT FK_Product_Category
        FOREIGN KEY(CategoryID)
        REFERENCES Categories(CategoryID),

    CONSTRAINT FK_Product_Supplier
        FOREIGN KEY(SupplierID)
        REFERENCES Suppliers(SupplierID)
);