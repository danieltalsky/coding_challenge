import pytest

from app.organization import InvalidOrganizationName, Organization


@pytest.mark.parametrize(
    "organization_name,is_valid",
    [
        # pass
        ("regularstring", True),
        ("string-with-hyphens", True),
        ("has-39-chaaaaaaaaaaaaaaaaaaaaaaaracters", True),
        ("w1th-numb3r5", True),
        ("UpperCase", True),
        # fail
        ("under_score", False),
        ("non-@lpha", False),
        ("-begins-with-hyphen", False),
        ("ends-with-hyphen-", False),
        ("double--hyphen", False),
        ("has-40-chaaaaaaaaaaaaaaaaaaaaaaaaracters", False),
    ]
)
def test_valid_name_check(organization_name: str, is_valid: bool):
    assert is_valid == Organization.is_valid_name(organization_name)


def test_throws_invalid_organization_name():
    with pytest.raises(InvalidOrganizationName):
        Organization("--Invalid-Name")


@pytest.mark.skip(reason="Not Implemented")
def test_valid_json_data():
    pass
