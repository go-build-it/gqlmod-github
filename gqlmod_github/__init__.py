"""
Provider for GitHub's v4 GraphQL API.
"""
from gqlmod.helpers.urllib import UrllibJsonProvider


class GitHubProvider(UrllibJsonProvider):
    endpoint = 'https://api.github.com/graphql'

    def __init__(self, token=None, username=None, password=None, client_id=None, client_secret=None):
        self.token = token

    def modify_request(self, req):
        if self.token:
            req.add_header('Authorization', f"Bearer {self.token}")
