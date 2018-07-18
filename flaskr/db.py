""" Connect to the Database. """
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """ Creates connection to database

        <g> is a special object that is unique for each request.
        It stores data that might be accessed by multiple functions
        during a request.

        <current_app> points to the Flask application handling the
        request (app factory)

        sqlite3.connect() establishes a connection to the file pointed
        at by the <DATABASE> configuration key.

        sqlite3.Row() tells the connection to return rows that behave
        like dicts (easier to access columns by name)
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """ closes connection to database"""
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """ Initialize a database 
    
        open_resource() opens a file relative to the flaskr package.
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """ Clear the existing data and create new tables. 
        
        click.command() defines a command line cmd called <init-db>
        that calls the init_db() function and shows a success msg to user.
    """
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """ Register with the applcation.

        The close_db() and init_db_command() functions need to be 
        registered with the appliction instance.
        Takes an application and does the registration

        app.teardown_appcontext() tells Flask to call that function
        when cleaning up after returning the response

        app.cli.add_command() adds a new command that can be calle with the
        flask command.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

