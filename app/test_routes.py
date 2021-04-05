import pytest

import app.routes


# @TODO: Better to do integration/functional tests here or as a separate Docker container?
# @TODO: Have separate configurations for test and regular so the tests can mock the network
@pytest.fixture
def client():
    with app.routes.app.test_client() as client:
        yield client


def test_health_check(client):
    rv = client.get("/health-check")
    assert rv.data == b"All Good!"


def test_invalid_org_name(client):
    rv = client.get("/organization/--invalid")
    assert rv.data == b"Invalid organization name."


@pytest.mark.skip(reason="Not Implemented")
def test_all_endpoints():
    # @TODO: Test all endpoints, and combinations
    pass
