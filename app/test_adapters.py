import pytest

from app.adapters import get_org_data_for_github
from app.organization import Organization


class Api:
    """ Simplest possible mocked API """
    @classmethod
    def pull(cls, url):
        return [
                {"fork": False}
            ]


def test_github_adapter_with_simple_response():
    org = Organization("test")
    org = get_org_data_for_github(org, Api())
    assert org.total_repos_original == 1


@pytest.mark.skip(reason="Not Implemented")
def test_more_complex_tests():
    # @TODO: Test with and without languages
    # @TODO: Test with and without tags
    # @TODO: Test API versions
    # @TODO: Test duplicates, etc.
    pass
