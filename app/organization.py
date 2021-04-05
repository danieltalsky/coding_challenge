import re
from typing import Set


class InvalidOrganizationName(Exception):
    """ Organization names can only contain certain characters """
    pass


class Organization:

    name: str
    VALID_NAME_REGEX = r'^[a-zA-Z\d](?:[a-zA-Z\d]|-(?=[a-zA-Z\d])){0,38}$'

    # profile should include the following information (when available):
    # Total number of public repos (separate by original repos vs forked repos)
    total_repos_original: int
    total_repos_forked: int

    # Total watcher/follower count
    total_followers: int

    # A list/count of languages used across all public repos
    repo_languages: Set[str]

    # A list/count of repo topics
    repo_topics: Set[str]

    def __init__(self, name):
        if not self.is_valid_name(name):
            raise InvalidOrganizationName
        self.name = name
        self.total_repos_original = 0
        self.total_repos_forked = 0
        self.total_followers = 0
        self.repo_languages = set()
        self.repo_topics = set()

    @classmethod
    def is_valid_name(cls, name: str):
        """
        Validates that the name is actually a valid GitLab and Github URL segment format

        Adapted from:
        https://github.com/shinnn/github-username-regex
        According to the form validation messages on Join Github page,
        - Github username may only contain alphanumeric characters or hyphens, no underscores
        - Github username cannot have multiple consecutive hyphens.
        - Github username cannot begin or end with a hyphen.
        - Maximum is 39 characters.
        """
        # @TODO compile the regex only once in the module or iterate chars?
        valid_name = re.compile(cls.VALID_NAME_REGEX)
        return bool(valid_name.match(name))

    @property
    def json_data(self):
        """ Assemble dict for json response """
        organization_details = {
            "total_repos_original": self.total_repos_original,
            "total_repos_forked": self.total_repos_forked,
            "total_followers": self.total_followers,
            "total_repo_languages": len(self.repo_languages),
            "repo_languages": list(self.repo_languages),
            "total_repo_topics": len(self.repo_topics),
            "repo_topics": list(self.repo_topics)
        }
        data = {
            "name": self.name,
            "organization_details": organization_details
        }
        return data
