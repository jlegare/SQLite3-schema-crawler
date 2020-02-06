# SQLite3 Schema Crawler

Generate a [GraphViz](https://graphviz.gitlab.io) dot file give a [SQLite3](https://www.sqlite.org/index.html) schema.

## Table of Contents

* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)

## Requirements

* [Python 3.8 or newer](https://www.python.org/downloads/)

## Installation

Clone this repository using:
```
git clone https://github.com/jlegare/SQLite3-schema-crawler.git
```

## Usage

To generate a GraphViz drawing for a SQLite3 database, provide the path to the database file on the command-line:
```
python schema-crawler.py some-database.sqlite3
```
