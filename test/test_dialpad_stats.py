"""
Tests for `dialpad-stats` module.
"""
# nosetests --verbosity=2 test/test_dialpad_stats.py
from unittest.mock import Mock, patch
from nose.tools import assert_is_not_none, assert_true
from dialpad_stats.dialpad import DialpadStats
import pytest

@pytest.fixture
def expected_export_id_response():
    return {
        "request_id": "12345abcde"
    }

@pytest.fixture
def expected_download_url_response():
    return {
        "status": "complete",
        "download_url": ""
    }


@patch('dialpad_stats.dialpad.requests.post')
def test_get_stats_export_id(mock_get, expected_export_id_response):
    dp = DialpadStats('12345', 'https://dialpad.com/api/v2')

    # mock_get.return_value = Mock(ok=True)
    mock_get.return_value = "12345abcde"
    expected_response = expected_export_id_response

    response_request_id = dp.get_stats_export_id(timezone='America/Los_Angeles', days_ago_start=1, days_ago_end=1, export_type='record', stat_type='calls')

    assert response_request_id == expected_response[request_id]

    # assert_is_not_none(response_request_id)
    # assert_true(mock_get.ok)
    # assert 'request_id' in mock_get.return_value.json.return_value


@patch('dialpad_stats.dialpad.requests.get')
def test_get_stats_download_url(mock_get, expected_download_url_response):
    dp = DialpadStats('12345', 'https://dialpad.com/api/v2')

    resp = {
        "status": "complete",
        "download_url": "12345abcde.csv"
    }

    # mock_get.return_value = Mock(ok=True)
    mock_get.return_value.json.return_value = resp

    response_download_url = dp.get_stats_download_url('12345')

    # assert_is_not_none(response_download_url)
    # assert_true(mock_get.ok)
    # assert 'download_url' in mock_get.return_value.json.return_value
