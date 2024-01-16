import pytest
from modules.api.clients.github import GithHub


@pytest.mark.api
def test_user_exists(github_api):
    user = github_api.get_user("defunkt")
    assert user["login"] == "defunkt"


@pytest.mark.api
def test_user_not_exists(github_api):
    r = github_api.get_user("butenkosergii")
    assert r["message"] == "Not Found"


@pytest.mark.api
def test_repo_can_be_found(github_api):
    r = github_api.search_repo("become-qa-auto")
    assert r["total_count"] == 54
    assert "become-qa-auto" in r["items"][0]["name"]


@pytest.mark.api
def test_repo_cannot_be_found(github_api):
    r = github_api.search_repo("sergiibutenko_repo_non_exist")
    assert r["total_count"] == 0


@pytest.mark.api
def test_repo_with_single_char_can_be_found(github_api):
    r = github_api.search_repo("s")
    assert r["total_count"] != 0


@pytest.mark.api
def test_emoji_exists(github_api):
    r = github_api.get_emoji()
    assert "alien" in r
    assert (
        r.get("alien")
        == "https://github.githubassets.com/images/icons/emoji/unicode/1f47d.png?v8"
    )


@pytest.mark.api
def test_emoji_non_exists(github_api):
    r = github_api.get_emoji()
    assert "qa" not in r


@pytest.mark.api
def test_commit_can_be_found(github_api):
    r = github_api.get_commit("octocat", "Hello-World")
    assert r[0]["commit"]["author"]["name"] == "The Octocat"
    assert r[0]["commit"]["author"]["email"] == "octocat@nowhere.com"
