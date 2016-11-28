import os

import pytest

from studentit.bookit.api import ApiClient


@pytest.fixture()
def client(monkeypatch):
	# Disble login
	monkeypatch.setattr('studentit.bookit.api.api_adapter.ApiAdapter._do_login', lambda x: None)

	return ApiClient(
		username='username',
		password='password'
	)


def test_api_client_should_have_api_adapter(client):
	assert client.adapter._logged_in == True
