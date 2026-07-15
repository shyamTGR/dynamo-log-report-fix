import json
from pathlib import Path

REPORT = Path("/app/report.json")

# Ground truth derived by hand from the fixed input environment/access.log:
# 6 request lines; distinct IPs {192.168.0.1, 192.168.0.2, 10.0.0.5};
# path counts /index.html=3, /about.html=2, /api/login=1.
EXPECTED_TOTAL_REQUESTS = 6
EXPECTED_UNIQUE_IPS = 3
EXPECTED_TOP_PATH = "/index.html"


def _report():
    return json.loads(REPORT.read_text())


def test_report_exists_and_is_json_object():
    """Criterion 1: /app/report.json exists and contains a single valid JSON object."""
    assert REPORT.exists(), "no /app/report.json found"
    assert isinstance(_report(), dict), "report.json must contain a single JSON object"


def test_report_has_exactly_required_keys():
    """Criterion 2: the object has exactly the keys total_requests, unique_ips, top_path."""
    assert set(_report().keys()) == {"total_requests", "unique_ips", "top_path"}


def test_total_requests_value():
    """Criterion 3: total_requests is the integer count of request lines in the log."""
    value = _report()["total_requests"]
    assert isinstance(value, int) and not isinstance(value, bool)
    assert value == EXPECTED_TOTAL_REQUESTS


def test_unique_ips_value():
    """Criterion 4: unique_ips is the integer count of distinct client IP addresses."""
    value = _report()["unique_ips"]
    assert isinstance(value, int) and not isinstance(value, bool)
    assert value == EXPECTED_UNIQUE_IPS


def test_top_path_value():
    """Criterion 5: top_path is the most frequently requested path."""
    value = _report()["top_path"]
    assert isinstance(value, str)
    assert value == EXPECTED_TOP_PATH
