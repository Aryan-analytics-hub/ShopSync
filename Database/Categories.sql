CREATE TABLE Categories
(
    CategoryID INT IDENTITY(1,1) PRIMARY KEY,

    CategoryName VARCHAR(100) NOT NULL UNIQUE,

    Description VARCHAR(255)
);