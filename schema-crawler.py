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
