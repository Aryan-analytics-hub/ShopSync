CREATE TABLE Suppliers
(
    SupplierID INT IDENTITY(1,1) PRIMARY KEY,

    SupplierName VARCHAR(100) NOT NULL,

    ContactPerson VARCHAR(100),

    Phone VARCHAR(15),

    Email VARCHAR(100) UNIQUE,

    Address VARCHAR(255)
);