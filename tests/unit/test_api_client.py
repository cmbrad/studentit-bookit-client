import os
import pytest
import fluentmock

from bookit.api_client import ApiClient


@pytest.fixture()
def client():
	return ApiClient(
		username=os.environ['BOOKIT_USERNAME'],
		password=os.environ['BOOKIT_PASSWORD']
	)


def test_describe_resource_by_name_should_except_if_resource_does_not_exist(client):
	pass

