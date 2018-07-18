""" Tests for blog views
    
    Call auth.login() and subsequent requests from the client will be
    logged in as the test user
"""
import pytest
from flaskr.db import get_db


def test_index(client, auth):
    """ Test index view

        Displays info about the post that was added with the test data.
        Edit link for each post by logged in user.
        Links to log in or register when not logged in
        Link to log out when logged in
    """
    response = client.get('/')
    assert b'Log In' in response.data
    assert b'Register' in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2018-01-01' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/1/update"' in response.data


@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
))

def test_login_required(client, path):
    """ Test user login
    
        A user must be logged in to access the create, 
        update and delete views
    """
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'


def test_author_required(app, client, auth):
    """ The logged in user must be the author of the post to access update and
        delete, otherise a 403 Forbidden status is returned.
    """
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()

    auth.login()
    # current user can't modify othe user's post
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    # Current user doesn't see edit link
    assert b'href="/1/update"' not in client.get('/').data


@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))

def test_exists_required(client, auth, path):
    """ If a post with the given id doesnt exist, update and delete 
        should return 404 Not Found.
    """
    auth.login()
    assert client.post(path).status_code == 404
