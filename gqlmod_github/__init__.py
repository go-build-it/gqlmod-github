"""
Provider for GitHub's v4 GraphQL API.
"""
import itertools
import importlib.resources

import graphql

from gqlmod.helpers.urllib import UrllibJsonProvider
from gqlmod.helpers.utils import walk_query, walk_variables, unwrap_type


def find_directive(ast_node, name):
    if ast_node is None:
        return
    for d in ast_node.directives:
        if d.name.value == name:
            break
    else:
        return

    return {
        arg.name.value: graphql.value_from_ast_untyped(arg.value)
        for arg in d.arguments
    }


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
        previews = set()
        # Find all the @preview directives and pull out their names
        for field in itertools.chain(
            (f for _, _, f in walk_query(gast, schema)),
            (f for _, f in walk_variables(gast, schema)),
        ):
            d = find_directive(field.ast_node, 'preview')
            if d and 'toggledBy' in d:
                previews.add(d['toggledBy'])

            typ, *_ = unwrap_type(field.type)
            d = find_directive(typ.ast_node, 'preview')
            if d and 'toggledBy' in d:
                previews.add(d['toggledBy'])
        return {
            '__previews': previews,
        }
