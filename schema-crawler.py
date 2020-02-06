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

    parser.add_argument ("-p", "--prefix-exclude", help = "exclude tables whose name starts with prefix", action = "append")
    parser.add_argument ("-e", "--exclude",        help = "exclude tables by name", action = "append")
    parser.add_argument ("database",               help = "path to SQLite3 database")

    arguments = parser.parse_args ()

    return { "database":         arguments.database,
             "excludes":         arguments.exclude if arguments.exclude else [ ],
             "exclude prefixes": arguments.prefix_exclude if arguments.prefix_exclude else [ ], }


def schema_of (configuration):
    def columns (table, connection):
        def column (info, names):
            return { "column name": info[names["name"]],
                     "type":        info[names["type"]],
                     "nullable":    info[names["notnull"]] == "1",
                     "default":     None if info[names["dflt_value"]] == "" else info[names["dflt_value"]],
                     "is pk":       info[names["pk"]] == "1", }

        # Technically, there's a SQL injection attack lurking here: we should never use Python string operations to
        # composed SQL statements. However, the underlying DB-API library's parameter substitution mechanism cannot be
        # used to substitute in objects ... only values, and furthermore the table names were pulled from the database,
        # so the tables already exists. In other words: had there been a problem, it would've happened before this whole
        # program even started executing.
        #
        cursor = connection.execute ("PRAGMA table_info (\"" + table["table name"] + "\");")

        return [ column (info, names_of (cursor)) for info in cursor ]


    def foreign_keys (table, connection):
        def foreign_key (info, names):
            return { "table name":       info[names["table"]],
                     "from column name": info[names["from"]],
                     "to column name":   info[names["to"]], }

        # See the comment elsewhere about a potential SQL injection attack.
        #
        cursor = connection.execute ("PRAGMA foreign_key_list (\"" + table["table name"] + "\");")

        return [ foreign_key (info, names_of (cursor)) for info in cursor ]


    def names_of (cursor):
        return { description[0]: index for ( index, description ) in enumerate (cursor.description) }


    def tables (connection, configuration):
        cursor = connection.execute ("SELECT name FROM sqlite_master WHERE type=\"table\";")

        for result in cursor:
            table_name = result[names_of (cursor)["name"]]

            if table_name in configuration["excludes"]:
                pass

            elif any ([ table_name.startswith (prefix) for prefix in configuration["exclude prefixes"] ]):
                pass

            else:
                yield { "table name": table_name, }


    connection = sqlite3.connect (configuration["database"])
    schema     = { "tables": list (tables (connection, configuration)) }

    for table in schema["tables"]:
        table["columns"]      = columns (table, connection)
        table["foreign keys"] = foreign_keys (table, connection)

    return schema

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
    def columns (table, connection):
        def column (info, names):
            return { "column name": info[names["name"]],
                     "type":        info[names["type"]],
                     "nullable":    info[names["notnull"]] == "1",
                     "default":     None if info[names["dflt_value"]] == "" else info[names["dflt_value"]],
                     "is pk":       info[names["pk"]] == "1", }

        # Technically, there's a SQL injection attack lurking here: we should never use Python string operations to
        # composed SQL statements. However, the underlying DB-API library's parameter substitution mechanism cannot be
        # used to substitute in objects ... only values, and furthermore the table names were pulled from the database,
        # so the tables already exists. In other words: had there been a problem, it would've happened before this whole
        # program even started executing.
        #
        cursor = connection.execute ("PRAGMA table_info (\"" + table["table name"] + "\");")

        return [ column (info, names_of (cursor)) for info in cursor ]


    def foreign_keys (table, connection):
        def foreign_key (info, names):
            return { "table name":       info[names["table"]],
                     "from column name": info[names["from"]],
                     "to column name":   info[names["to"]], }

        # See the comment elsewhere about a potential SQL injection attack.
        #
        cursor = connection.execute ("PRAGMA foreign_key_list (\"" + table["table name"] + "\");")

        return [ foreign_key (info, names_of (cursor)) for info in cursor ]


    def names_of (cursor):
        return { description[0]: index for ( index, description ) in enumerate (cursor.description) }


    def tables (connection, configuration):
        cursor = connection.execute ("SELECT name FROM sqlite_master WHERE type=\"table\";")

        for result in cursor:
            table_name = result[names_of (cursor)["name"]]

            if table_name in configuration["excludes"]:
                pass

            elif any ([ table_name.startswith (prefix) for prefix in configuration["exclude prefixes"] ]):
                pass

            else:
                yield { "table name": table_name, }


    configuration = configure ()

    schema = schema_of (configuration)
