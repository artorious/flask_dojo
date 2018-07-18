""" Authorization tests """
import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    """ Test user registration 
        
        Make a GET request and return the Response object returned by Flask.
        To test that a page renders successfully, a simple request is made
        and checked for a 200 OK status_code. 500 Internal Server Error code
        is returned on failure.

        Make a POST request, converting the <data> dict into form data.
        <headers> will have a <Location> header with the login URL when the 
        register view redirects to the login view.
        <data> contains the body of the response as bytes

    """
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert get_db().execute(
            "select * from user where username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametriz(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))

def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data

