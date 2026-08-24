"""Tests for the bounty-dashboard empty-data guard (fixes #106)."""
import importlib.util
import os

_HERE = os.path.dirname(__file__)
_MODPATH = os.path.abspath(os.path.join(_HERE, "..", "scripts", "build-bounty-dashboard.py"))

_spec = importlib.util.spec_from_file_location("build_bounty_dashboard", _MODPATH)
_bbd = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_bbd)
should_overwrite_dashboard = _bbd.should_overwrite_dashboard


def test_nonempty_current_always_overwrites():
    assert should_overwrite_dashboard(prev_total=100, current_total=50) is True
    assert should_overwrite_dashboard(prev_total=0, current_total=1) is True


def test_empty_current_over_empty_prev_is_allowed():
    # No previous data to protect; first successful empty run is fine.
    assert should_overwrite_dashboard(prev_total=0, current_total=0) is True


def test_empty_current_over_populated_prev_is_blocked():
    # The regression from #106: never clobber live data with an empty refresh.
    assert should_overwrite_dashboard(prev_total=100, current_total=0) is False
    assert should_overwrite_dashboard(prev_total=5, current_total=0) is False
