import pytest
from mock import patch

from studentit.bookit.api import ApiClient


@patch('studentit.bookit.api.api_adapter.ApiAdapter._do_login')
@pytest.fixture()
def client(monkeypatch):
    return ApiClient(
        username='username',
        password='password'
    )


def test_api_client_should_have_api_adapter(client):
    assert not client.adapter._logged_in
