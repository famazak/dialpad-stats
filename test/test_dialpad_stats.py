"""
Tests for `dialpad-stats` module.
"""
# nosetests --verbosity=2 test/test_dialpad_stats.py
from unittest.mock import Mock, patch
from nose.tools import assert_is_not_none, assert_true
from dialpad_stats.dialpad import DialpadStats


@patch('dialpad_stats.dialpad.requests.post')
def test_get_stats_export_id(mock_get):
    dp = DialpadStats('12345', 'https://dialpad.com/api/v2')
    
    resp = {
        "request_id": "12345abcde"
    }

    mock_get.return_value = Mock(ok=True)
    mock_get.return_value.json.return_value = resp

    response_request_id = dp.get_stats_export_id(timezone='America/Los_Angeles', days_ago_start=1, days_ago_end=1, export_type='record', stat_type='calls')

    assert_is_not_none(response_request_id)
    assert_true(mock_get.ok)
    assert 'request_id' in mock_get.return_value.json.return_value