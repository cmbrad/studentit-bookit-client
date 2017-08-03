import os
from pathlib import Path

import pytest
from mock import patch, MagicMock

from studentit.bookit.api import ApiClient


@patch('studentit.bookit.api.api_adapter.ApiAdapter._do_login')
@pytest.fixture()
def client(monkeypatch):
    return ApiClient(
        username='username',
        password='password'
    )


def test_admin_location_status_should_return_status_of_all_resources(client):
    get_mock = MagicMock()
    get_mock.return_value.text = read_data('admin_location.html')
    with patch('studentit.bookit.api.api_client.ApiAdapter.get', get_mock):
        assert client.admin_location_status(location_id=7) == {
            897: {'name': 'Booth 4', 'state': 'Switched Off or No Communication'},
            898: {'name': 'Booth 5', 'state': 'Switched Off or No Communication'},
            899: {'name': 'Booth 6', 'state': 'Switched Off or No Communication'},
            900: {'name': 'Booth 7', 'state': 'Switched Off or No Communication'},
            901: {'name': 'Booth 8', 'state': 'Switched Off or No Communication'},
            902: {'name': 'Booth 9', 'state': 'Switched Off or No Communication'},
            903: {'name': 'Booth 10', 'state': 'Switched Off or No Communication'},
            904: {'name': 'Booth 11', 'state': 'Switched Off or No Communication'},
            905: {'name': 'Project Room 10', 'state': 'Switched Off or No Communication'},
        }


def test_available_start_time_by_resource_id_should_return_a_list_of_start_time(client):
    get_mock = MagicMock()
    get_mock.return_value.text = read_data('resource_id.html')
    with patch('studentit.bookit.api.api_client.ApiAdapter.get', get_mock):
        assert client.available_start_time_by_resource_id(900) == ['18:00:00', '20:30:00']


def test_list_bookings_should_return_a_list_of_bookings(client):
    get_mock = MagicMock()
    get_mock.return_value.text = read_data('list_bookings.html')
    with patch('studentit.bookit.api.api_client.ApiAdapter.get', get_mock):
        assert client.list_bookings() == [
            {
                'booking_date': '01/08/2017',
                'start_time': '21:00',
                'end_time': '21:30',
                'duration': '00:30:00',
                'site': 'Baillieu',
                'location': ':Group Spaces North',
                'resource': 'Booth 4',
                'booking_id': '3499581'
            },
            {
                'booking_date': '01/08/2017',
                'start_time': '22:00',
                'end_time': '22:30',
                'duration': '00:30:00',
                'site': 'Baillieu',
                'location': ':Group Spaces North',
                'resource': 'Booth 4',
                'booking_id': '3499583'
            },
            {
                'booking_date': '01/08/2017',
                'start_time': '23:00',
                'end_time': '23:30',
                'duration': '00:30:00',
                'site': 'Baillieu',
                'location': ':Group Spaces North',
                'resource': 'Booth 5',
                'booking_id': '3499586'
            },
        ]


def test_delete_booking_should_raise_exception_on_error(client):
    post_mock = MagicMock()
    post_mock.return_value.text = read_data('delete_booking_fail.html')
    with patch('studentit.bookit.api.api_client.ApiAdapter.post', post_mock):
        with pytest.raises(Exception) as e:
            client.delete_booking('3499581', False)
        assert 'Unexpected error: Input string was not in a correct format.Object reference not set to an instance ' \
               'of an object.' in str(e)


def test_delete_booking_should_return_true_on_success(client):
    post_mock = MagicMock()
    post_mock.return_value.text = read_data('delete_booking_success.html')
    with patch('studentit.bookit.api.api_client.ApiAdapter.post', post_mock):
        assert client.delete_booking('3499581', False)


def test_create_booking_should_return_true_on_success(client):
    post_mock = MagicMock()
    post_mock.return_value.text = read_data('create_booking_success.html')
    with patch('studentit.bookit.api.api_client.ApiAdapter.post', post_mock):
        assert client.create_booking('18:00:00', '18:30:00', '01-08-2017', 900, False)


def test_create_booking_should_raise_exception_on_error(client):
    post_mock = MagicMock()
    post_mock.return_value.text = read_data('create_booking_fail.html')
    with patch('studentit.bookit.api.api_client.ApiAdapter.post', post_mock):
        with pytest.raises(Exception) as e:
            client.create_booking('18:00:00', '18:30:00', '01-08-2017', 900, False)
        assert 'Booking overlapped!' in str(e)


def read_data(data_name):
    data_dir = Path(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')).resolve()
    file_path = os.path.join(data_dir, data_name)
    with open(file_path, 'r') as f:
        return f.read()
