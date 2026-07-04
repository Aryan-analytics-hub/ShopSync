import pyodbc
from config import CONNECTION_STRING


def get_connection():
    return pyodbc.connect(CONNECTION_STRING)


def execute_query(query, params=None):
    """
    Executes INSERT, UPDATE and DELETE queries.
    """

    conn = get_connection()
    cursor = conn.cursor()

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    conn.commit()
    conn.close()


def fetch_all(query, params=None):
    """
    Executes SELECT queries and returns all rows.
    """

    conn = get_connection()
    cursor = conn.cursor()

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    rows = cursor.fetchall()

    conn.close()

    return rows


def fetch_one(query, params=None):
    """
    Executes SELECT queries and returns one row.
    """

    conn = get_connection()
    cursor = conn.cursor()

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    row = cursor.fetchone()

    conn.close()

    return row