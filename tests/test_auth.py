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
        
        pytest.mark.parametrize tells Pytest to run the same test function 
        with different arguments.
        Tests different invalid input and error messages
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


@pytest.mark.parametrize(('username', 'password', 'message'), (
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


def test_login(client, auth):
    """ Tests user login

        Make a GET request and return the Response object returned by Flask.
        To test that a page renders successfully, a simple request is made
        and checked for a 200 OK status_code. 500 Internal Server Error code
        is returned on failure.
        
        Rather than testing the data in the database, session should have
        user_id set ater logging in.

        Using <client> in a <with> block allows accessing context variables
        such as session after the response is returned.

        pytest.mark.parametrize tells Pytest to run the same test function 
        with different arguments.
        Tests different invalid input and error messages
    """
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))

def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


