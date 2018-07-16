""" Tests for App factory """
from flaskr import create_app


def test_config():
    """ Test that If config is not passed, default configuration used.
        Otherwise the configuration should be overridden
    """
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    """ Test that response data matches """
    response = client.get('/hello')
    assert response.data == b'Hello World'
