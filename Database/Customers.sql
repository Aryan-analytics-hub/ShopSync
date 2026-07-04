CREATE TABLE Customers
(
    CustomerID INT IDENTITY(1,1) PRIMARY KEY,

    FirstName VARCHAR(50) NOT NULL,

    LastName VARCHAR(50),

    Email VARCHAR(100) UNIQUE,

    Phone VARCHAR(15) UNIQUE,

    Address VARCHAR(255),

    City VARCHAR(50),

    State VARCHAR(50),

    PostalCode VARCHAR(10),

    CreatedAt DATETIME2 DEFAULT GETDATE()
);