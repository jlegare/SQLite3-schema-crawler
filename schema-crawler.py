# ----------------------------------------
# IMPORTS
# ----------------------------------------

import argparse
import json
import logging
import sqlite3

# ----------------------------------------
# GLOBALS
# ----------------------------------------

DEBUGGING = True

# ----------------------------------------
# FUNCTIONS
# ----------------------------------------

def configure ():
    parser = argparse.ArgumentParser (description = "Collect SQLite3 database schema information.")

    parser.add_argument ("database", help = "paths to SQLite3 database")

    arguments = parser.parse_args ()

    return { "database": arguments.database, }

# ----------------------------------------
# MAIN PROCESSING
# ----------------------------------------

if __name__ == "__main__":
    # Configure the log system.
    #
    global LOGGER

    logging.basicConfig (format = ("------------------------------------------------------------------------\n"
                                   + "%(name)s:%(levelname)s:\n%(message)s\n"),
                         level = logging.DEBUG if DEBUGGING else logging.INFO)

    LOGGER = logging.getLogger (__name__)


if __name__ == "__main__":
    def column_names (cursor):
        return { description[0]: index for ( index, description ) in enumerate (cursor.description) }


    def columns (table, connection):
        def column (info, column_names):
            return { "name":     info[column_names["name"]],
                     "type":     info[column_names["type"]],
                     "nullable": info[column_names["notnull"]] == "1",
                     "default":  None if info[column_names["dflt_value"]] == "" else info[column_names["dflt_value"]],
                     "is pk":    info[column_names["pk"]] == "1" }

        # Technically, there's a SQL injection attack lurking here: we should never use Python string operations to
        # composed SQL statements. However, the underlying DB-API library's parameter substitution mechanism cannot be
        # used to substitute in objects ... only values, and furthermore the table names were pulled from the database,
        # so the tables already exists. In other words: had there been a problem, it would've happened before this whole
        # program even started executing.
        #
        cursor = connection.execute ("PRAGMA table_info (\"" + table["name"] + "\");")

        return [ column (info, column_names (cursor)) for info in cursor ]


    def tables (connection):
        cursor = connection.execute ("SELECT name FROM sqlite_master WHERE type=\"table\";")

        return [ { "name": result[column_names (cursor)["name"]] } for result in cursor ]


    configuration = configure ()

    connection = sqlite3.connect (configuration["database"])
    schema     = { "tables": tables (connection) }

    for table in schema["tables"]:
        table["columns"] = columns (table, connection)
