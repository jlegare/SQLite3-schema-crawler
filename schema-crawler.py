# ----------------------------------------
# IMPORTS
# ----------------------------------------

import argparse
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
    def tables (connection):
        return [ { "table name": result[0] }
                 for result in connection.cursor ().execute ("SELECT name FROM sqlite_master WHERE type=\"table\";") ]


    configuration = configure ()
    connection    = sqlite3.connect (configuration["database"])
    schema        = { "tables": tables (connection) }
