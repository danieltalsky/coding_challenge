import pytest

import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """ endpoint health check """
    rv = client.get('/health-check')
    assert b'All Good!' in rv.data
