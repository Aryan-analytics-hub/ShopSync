"""Application and database configuration.

Values in ``config.ini`` can be changed for each desktop installation.  The
same values may be overridden with SHOPSYNC_DB_* environment variables, which
is useful for managed deployments.
"""

import configparser
import os
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else BASE_DIR
# An adjacent config.ini takes precedence in a packaged deployment so database
# settings can be changed without rebuilding the executable.
CONFIG_PATH = Path(os.getenv("SHOPSYNC_CONFIG", RUNTIME_DIR / "config.ini"))
ASSETS_DIR = BASE_DIR / "assets"


def _load_settings():
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH, encoding="utf-8")
    section = parser["database"] if parser.has_section("database") else {}

    def get(name, default):
        return os.getenv(f"SHOPSYNC_DB_{name.upper()}", section.get(name, default))

    return {
        "driver": get("driver", "ODBC Driver 17 for SQL Server"),
        "server": get("server", r"localhost\\SQLEXPRESS"),
        "database": get("database", "ShopSyncDB"),
        "trusted_connection": get("trusted_connection", "yes"),
        "username": get("username", ""),
        "password": get("password", ""),
    }


DATABASE_CONFIG = _load_settings()
SERVER = DATABASE_CONFIG["server"]
DATABASE = DATABASE_CONFIG["database"]


def build_connection_string(settings=DATABASE_CONFIG):
    """Build the SQL Server ODBC string without embedding machine-specific data."""
    parts = [
        f"DRIVER={{{settings['driver']}}}",
        f"SERVER={settings['server']}",
        f"DATABASE={settings['database']}",
    ]
    if settings["username"]:
        parts.extend((f"UID={settings['username']}", f"PWD={settings['password']}"))
    else:
        parts.append(f"Trusted_Connection={settings['trusted_connection']}")
    return ";".join(parts) + ";"


CONNECTION_STRING = build_connection_string()
