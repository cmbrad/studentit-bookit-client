import os
import pytest
import fluentmock

import bookit
from bookit.api_client import ApiClient


@pytest.fixture()
def client(monkeypatch):
	# Disble login
	monkeypatch.setattr('bookit.api_adapter.ApiAdapter._do_login', lambda x: None)

	return ApiClient(
		username=os.environ['BOOKIT_USERNAME'],
		password=os.environ['BOOKIT_PASSWORD']
	)


def test_describe_resource_by_name_should_except_if_resource_does_not_exist(client):
	pass

