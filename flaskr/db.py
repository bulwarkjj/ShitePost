"""
Creating sqlite instance to hold users and posts
- if I make the app bigger, I should really make a postgreSQL
"""
import sqlite3

import click
from flask import current_app, g 

# g -> used to store data that might be accessed by multiple funcitons during the request
# current_app -> points to flask app handling requests

def get_db():
    """
    Creating a connection to the sqlite db
    - all queries and operations will use this connection
    - in web apps, this connection will be tied to requests
        - created when handling requests and closed before request
            is sent
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """
    Checks if connection was created, if it exists then it is closed
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_db():
    """
    initalizing sqlite db instance
    """

    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode("utf8"))

@click.command("init-db")
def init_db_command():
    """
    clear the existing data and create new tables
    """

    init_db()
    click.echo("Initialized the database")