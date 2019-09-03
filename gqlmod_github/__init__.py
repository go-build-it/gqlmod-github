"""
Provider for GitHub's v4 GraphQL API.
"""
import importlib.resources

from gqlmod.helpers.urllib import UrllibJsonProvider


class GitHubProvider(UrllibJsonProvider):
    endpoint = 'https://api.github.com/graphql'

    def __init__(self, token=None, username=None, password=None, client_id=None, client_secret=None):
        self.token = token

    def modify_request(self, req):
        if self.token:
            req.add_header('Authorization', f"Bearer {self.token}")

    def get_schema_str(self):
        return importlib.resources.read_text(__name__, 'schema.graphql')

    def codegen_extra_kwargs(self, gast, schema):
        return {
            '__spam': 'eggs',
        }
