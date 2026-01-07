import logging
import datetime
from unittest.mock import patch, MagicMock, PropertyMock
# import pytest
import psutil
from functions.functions import is_thunderbird_running

import psutil

from functions.functions import (
    log_uncaught_exceptions,
    is_thunderbird_running,
    calc_duration,
    format_size,
)

# -------------------------------------------------
# log_uncaught_exceptions
# -------------------------------------------------
def test_log_uncaught_exceptions_logs_critical():
    with patch.object(logging, "critical") as mock_critical:
        exc = ValueError("boom")
        log_uncaught_exceptions(ValueError, exc, None)

        mock_critical.assert_called_once()
        args, kwargs = mock_critical.call_args
        assert args[0] == "Uncaught exception"
        assert "exc_info" in kwargs


# -------------------------------------------------
# is_thunderbird_running
# -------------------------------------------------
def test_is_thunderbird_running_true():
    mock_proc = MagicMock()
    mock_proc.info = {"name": "thunderbird.exe"}

    with patch.object(psutil, "process_iter", return_value=[mock_proc]):
        assert is_thunderbird_running() is True


def test_is_thunderbird_running_false():
    mock_proc = MagicMock()
    mock_proc.info = {"name": "python.exe"}

    with patch.object(psutil, "process_iter", return_value=[mock_proc]):
        assert is_thunderbird_running() is False


def test_is_thunderbird_running_handles_exceptions():
    # Create a mock process that raises AccessDenied when info is accessed
    mock_proc = MagicMock()
    type(mock_proc).info = PropertyMock(side_effect=psutil.AccessDenied())

    # Patch process_iter to return a list with our mock process
    with patch.object(psutil, "process_iter", return_value=[mock_proc]):
        # Should handle the AccessDenied and return False
        assert is_thunderbird_running() is False


# -------------------------------------------------
# calc_duration
# -------------------------------------------------
def test_calc_duration_under_one_minute():
    start = datetime.datetime(2024, 1, 1, 12, 0, 0, 0)
    end = datetime.datetime(2024, 1, 1, 12, 0, 10, 500000)

    result = calc_duration(start, end)

    assert result == "10.500 seconds"


def test_calc_duration_exactly_one_minute():
    start = datetime.datetime(2024, 1, 1, 12, 0, 0)
    end = datetime.datetime(2024, 1, 1, 12, 1, 5, 250000)

    result = calc_duration(start, end)

    assert result == "1 minute and 5.250 seconds"


def test_calc_duration_multiple_minutes():
    start = datetime.datetime(2024, 1, 1, 12, 0, 0)
    end = datetime.datetime(2024, 1, 1, 12, 3, 2, 0)

    result = calc_duration(start, end)

    assert result == "3 minutes and 2.0 seconds"


# -------------------------------------------------
# format_size
# -------------------------------------------------
def test_format_size_bytes():
    assert format_size(500) == "500.00 B"


def test_format_size_kilobytes():
    assert format_size(1024) == "1.00 KB"


def test_format_size_megabytes():
    assert format_size(1024 * 1024) == "1.00 MB"


def test_format_size_gigabytes():
    assert format_size(1024 * 1024 * 1024) == "1.00 GB"


def test_format_size_rounding():
    assert format_size(1536) == "1.50 KB"
