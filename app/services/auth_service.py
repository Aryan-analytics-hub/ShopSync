"""Authentication storage and password verification for ShopSync."""

import base64
import configparser
import hashlib
import hmac
import os

from config import CONFIG_PATH
from database import get_connection


PBKDF2_ITERATIONS = 310_000
VALID_ROLES = ("Admin", "Employee")


def hash_password(password):
    """Return a salted PBKDF2-SHA256 password value suitable for storage."""
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return "pbkdf2_sha256${}${}${}".format(
        PBKDF2_ITERATIONS,
        base64.b64encode(salt).decode("ascii"),
        base64.b64encode(digest).decode("ascii"),
    )


def verify_password(password, stored_value):
    try:
        algorithm, iterations, encoded_salt, encoded_digest = stored_value.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), base64.b64decode(encoded_salt), int(iterations)
        )
        return hmac.compare_digest(base64.b64encode(digest).decode("ascii"), encoded_digest)
    except (AttributeError, ValueError, TypeError):
        return False


def _initial_admin_settings():
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH, encoding="utf-8")
    section = parser["authentication"] if parser.has_section("authentication") else {}
    return (
        os.getenv("SHOPSYNC_INITIAL_ADMIN_USERNAME", section.get("initial_admin_username", "admin")),
        os.getenv("SHOPSYNC_INITIAL_ADMIN_PASSWORD", section.get("initial_admin_password", "ChangeMe123!")),
    )


def ensure_users_table():
    """Create the user table and first admin account if this is a new deployment."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            IF OBJECT_ID('dbo.Users', 'U') IS NULL
            CREATE TABLE dbo.Users (
                UserID INT IDENTITY(1,1) PRIMARY KEY,
                Username NVARCHAR(100) NOT NULL UNIQUE,
                PasswordHash NVARCHAR(500) NOT NULL,
                Role NVARCHAR(20) NOT NULL
                    CONSTRAINT CK_Users_Role CHECK (Role IN ('Admin', 'Employee')),
                IsActive BIT NOT NULL CONSTRAINT DF_Users_IsActive DEFAULT 1,
                CreatedAt DATETIME2 NOT NULL CONSTRAINT DF_Users_CreatedAt DEFAULT SYSDATETIME()
            )
            """
        )
        cursor.execute("SELECT COUNT(*) FROM dbo.Users")
        if cursor.fetchone()[0] == 0:
            username, password = _initial_admin_settings()
            cursor.execute(
                "INSERT INTO dbo.Users (Username, PasswordHash, Role) VALUES (?, ?, 'Admin')",
                (username.strip(), hash_password(password)),
            )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def authenticate(username, password):
    """Return the authenticated user as a dict, otherwise ``None``."""
    if not username or not password:
        return None
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT UserID, Username, PasswordHash, Role FROM dbo.Users WHERE Username = ? AND IsActive = 1",
            (username.strip(),),
        )
        row = cursor.fetchone()
        if row and verify_password(password, row.PasswordHash):
            return {"id": row.UserID, "username": row.Username, "role": row.Role}
        return None
    finally:
        cursor.close()
        conn.close()


def create_user(username, password, role="Employee"):
    """Create an account for an Admin or Employee (for admin tooling/scripts)."""
    if role not in VALID_ROLES:
        raise ValueError("Role must be Admin or Employee.")
    if not username or not password:
        raise ValueError("Username and password are required.")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO dbo.Users (Username, PasswordHash, Role) VALUES (?, ?, ?)",
            (username.strip(), hash_password(password), role),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()
