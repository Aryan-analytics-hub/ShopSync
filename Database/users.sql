CREATE TABLE Users
(
    UserID INT IDENTITY(1,1) PRIMARY KEY,

    Username VARCHAR(50) NOT NULL UNIQUE,

    PasswordHash VARCHAR(255) NOT NULL,

    FullName VARCHAR(100) NOT NULL,

    Email VARCHAR(100) NOT NULL UNIQUE,

    Role VARCHAR(20) NOT NULL
        CHECK (Role IN ('Admin','Manager','Sales')),

    CreatedAt DATETIME2 DEFAULT GETDATE()
);