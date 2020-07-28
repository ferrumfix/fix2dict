import sqlite3
from sqlite3 import Error
import pkg_resources

from .resources import PKG_NAME

def dict_to_mem_sqlite(data, conn):
    sql_setup = pkg_resources.resource_string(
        PKG_NAME, "resources/sql/setup.sql"
    )
    conn.executescript(sql_setup.decode("ascii"))
    for (key, val) in data["abbreviations"].items():
        conn.execute("INSERT INTO abbreviation (abbr, meaning) VALUES (?, ?);", (key, val["term"]))
    conn.commit()
    for (key, val) in data["datatypes"].items():
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM datatype WHERE name=?;", (val.get("base", None), ))
        rows = cursor.fetchall()
        if len(rows) >= 1:
            base = rows[0][0]
        else:
            base = None
        conn.execute("INSERT INTO datatype (name, base) VALUES (?, ?);", (key, base))
    conn.commit()
    for (key, val) in data["sections"].items():
        conn.execute("INSERT INTO section (name) VALUES (?);", (key, ))
    conn.commit()
    for (key, val) in data["categories"].items():
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM section WHERE name=?;", (val.get("section", None), ))
        rows = cursor.fetchall()
        if len(rows) >= 1:
            section = rows[0][0]
        else:
            section = None
        conn.execute("INSERT INTO category (name, kind, section) VALUES (?, ?, ?);", (key, val.get("kind", None), section))
    conn.commit()
    return conn
