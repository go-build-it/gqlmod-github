import pytest

import gqlmod
import gqlmod.enable  # noqa
import gqlmod_github
from gqlmod.providers import _mock_provider


class MockGithubProvider(gqlmod_github.GitHubProvider):
    def query_sync(self, query, variables):
        print("sync")
        self.last_query = query
        self.last_vars = variables

    async def query_async(self, query, variables):
        print("async")
        self.last_query = query
        self.last_vars = variables


def test_get_schema():
    assert gqlmod.providers.query_for_schema('github')


@pytest.mark.parametrize('name', ['queries', 'queries_sync', 'queries_async'])
def test_imports(name):
    mod = __import__(name)
    assert mod.__name__ == name


def test_import():
    import queries  # noqa
    prov = MockGithubProvider()
    with _mock_provider('github', prov):
        queries.Login()
        assert prov.last_vars['__previews'] == set()

        queries.start_check_run(repo=123, sha="beefbabe")
        assert prov.last_vars['__previews'] == set()

        queries.append_check_run(repo=123, checkrun=456)
        assert prov.last_vars['__previews'] == set()

        queries.get_label(repo=123, name="spam")
        assert prov.last_vars['__previews'] == set()

        queries.get_check_run(id=123)
        assert prov.last_vars['__previews'] == set()

        queries.go_deploy(id=123, repo=456)
        assert prov.last_vars['__previews'] == {"flash-preview"}


@pytest.mark.asyncio
async def test_async_import():
    import queries_async  # noqa

    assert queries_async.__file__.endswith('/queries.gql')

    prov = MockGithubProvider()
    with _mock_provider('github', prov):
        assert gqlmod.providers.get_provider('github') is prov

        await queries_async.Login()
        assert prov.last_vars['__previews'] == set()

        await queries_async.start_check_run(repo=123, sha="beefbabe")
        assert prov.last_vars['__previews'] == set()

        await queries_async.append_check_run(repo=123, checkrun=456)
        assert prov.last_vars['__previews'] == set()

        await queries_async.get_label(repo=123, name="spam")
        assert prov.last_vars['__previews'] == set()

        await queries_async.get_check_run(id=123)
        assert prov.last_vars['__previews'] == set()

        await queries_async.go_deploy(id=123, repo=456)
        assert prov.last_vars['__previews'] == {"flash-preview"}
