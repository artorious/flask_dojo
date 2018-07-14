import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    """ Create and open a temporary file returning the file object and the path
        to it. The database path is overridden so it points to this temporary 
        path instead of the instatnce folder. TESTING tells flask that the app
        is in testing mode. After setting the path,
        the database Tables are created and the test data is inserted.
        After the test is over, the temporary file is closed and removed
    """
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """ Calls app.test_client() with the <app> object created by the app
        fixture.
        Tests will use client to make requests to the application
        without running the server
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """ Creates a runner that can call the Click commands registered
        with the application.
    """
    return app.test_cli_runner()

