from app.network import Api
from app.organization import Organization

GITHUB_BASE = 'https://api.github.com/'
GITHUB_REPO_LIST = 'orgs/{org}/repos'


def get_org_data_for_github(org: Organization, api: Api, version=4, pull_all_languages=False, pull_all_tags=False):

    repos = api.pull(GITHUB_BASE + GITHUB_REPO_LIST.format(org=org.name))

    for repo in repos:

        # profile should include the following information (when available):
        # Total number of public repos (separate by original repos vs forked repos)
        if repo.get("fork", False):
            org.total_repos_forked += 1
        else:
            org.total_repos_original += 1

        # Total watcher/follower count
        # @FIXME: Watchers/followers for the org or repos?  Counting user overlap or not?
        # @FIXME: I'm doing a naive sum of all watchers/stargazers of each repo (could collect a user set)
        org.total_followers += repo.get("watchers_count", 0)

        # A list/count of languages used across all public repos
        # @FIXME: Did they mean ALL languages? Doing so, even though requires per-repo calls
        languages_url = repo.get("languages_url", False)
        if pull_all_languages and languages_url:
            languages = api.pull(languages_url)
            for language in languages.keys():
                org.repo_languages.add(language)

        # A list/count of repo topics
        # @FIXME: tags=topics, I'm assuming
        tags_url = repo.get("tags_url", False)
        if pull_all_tags and tags_url:
            tags = api.pull(tags_url)
            for tag in tags:
                org.repo_topics.add(tag)

    return org


BITBUCKET_BASE = 'https://api.bitbucket.org/2.0/'
BITBUCKET_REPO_LIST = 'repositories/{org}'


# @TODO: Use version information
def get_org_data_for_bitbucket(org: Organization, api: Api, version=2):

    records = api.pull(BITBUCKET_BASE + BITBUCKET_REPO_LIST.format(org=org.name))
    repos = records.get("values", [])

    for repo in repos:
        # profile should include the following information (when available):
        # Total number of public repos (separate by original repos vs forked repos)
        # @TODO: This isn't the accurate way to check forks for bitbucket, fix if time
        if repo.get("fork", False):
            org.total_repos_forked += 1
        else:
            org.total_repos_original += 1

        # Total watcher/follower count
        # @TODO: This is only grabbing the first page, and thus, isn't accurate, add pagination
        watchers_url = repo.get("links", {}).get("watchers", {}).get("href", False)
        if watchers_url:
            records = api.pull(watchers_url)
            org.total_followers += records.get("pagelen", 0)

        # A list/count of languages used across all public repos
        # @FIXME: Bitbucket only offers primary language
        language = repo.get("language", False)
        if language:
            org.repo_languages.add(language)

        # A list/count of repo topics
        # @FIXME: Don't see an analogue for repo "topics" in bitbucket

    return org
