import requests


class RateLimitExceeded(Exception):
    pass


# @TODO: Right now all network errors stop the whole process, more sophisticated network handling would be better
class ResourceNotFound(Exception):
    pass


class UnknownNetworkError(Exception):
    pass


class Api:
    """ Generic abstraction for network API calls allowing this object to be mocked for testing """

    # @TODO: store some state about retries, network state, etc.
    network_state: list

    def pull(self, url: str):
        """ Calls a URL and returns a data structure of its JSON """

        # @TODO: This is where a caching layer could be implemented
        response = requests.get(url)

        # @TODO: Handle network resilience, incremental backoff, some kind of async layer here
        self.network_state = []
        # @FIXME: NAIVELY ASSUMING 403's are rate limit errors
        if response.status_code == 403:
            raise RateLimitExceeded(url)

        # @TODO: DETECT 404's and throw specific error to handle in api output message
        if response.status_code == 404:
            raise ResourceNotFound(url)

        if response.status_code != 200:
            raise UnknownNetworkError(url)

        # @TODO: We're not paginating results or anything more sophisticated and would need to
        return response.json()
