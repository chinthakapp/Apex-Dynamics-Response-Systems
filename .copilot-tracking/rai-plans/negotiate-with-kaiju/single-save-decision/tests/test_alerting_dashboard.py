"""Tests for the alerting and dashboard modules using synthetic telemetry events."""
import importlib.util
import pathlib

tests_dir = pathlib.Path(__file__).parent


def _load(module_name, filename):
    spec = importlib.util.spec_from_file_location(module_name, str(tests_dir / "mocks" / filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


alerting = _load("alerting", "alerting.py")
dashboard = _load("dashboard", "dashboard.py")


def make_event(sequence, decision, decision_id="d-1", confidence=0.95):
    return {
        "sequence": sequence,
        "decision_id": decision_id,
        "aggregated_confidence": confidence,
        "decision": decision,
        "impact_level": "low",
        "audit_ref": "manifest.json",
    }


def test_alert_raised_for_missing_audit_record():
    events = [make_event(1, "missing_audit_record")]
    alerts = alerting.evaluate_alerts(events)
    assert len(alerts) == 1
    assert alerts[0]["severity"] == "critical"


def test_alert_raised_for_invalid_audit_signature():
    events = [make_event(1, "invalid_audit_signature")]
    alerts = alerting.evaluate_alerts(events)
    assert len(alerts) == 1
    assert alerts[0]["severity"] == "critical"


def test_alert_raised_for_low_confidence():
    events = [make_event(1, "low_confidence")]
    alerts = alerting.evaluate_alerts(events)
    assert len(alerts) == 1
    assert alerts[0]["severity"] == "warning"


def test_no_alert_for_plain_allow():
    events = [make_event(1, "allow"), make_event(2, "requires_approval")]
    alerts = alerting.evaluate_alerts(events)
    assert alerts == []


def test_repeated_allow_within_window_triggers_warning():
    events = [make_event(i, "allow", decision_id=f"d-{i}") for i in range(1, 4)]
    alerts = alerting.evaluate_alerts(events)
    assert any("possible poisoning" in a["reason"] for a in alerts)


def test_dashboard_summary_counts_and_alerts():
    events = [
        make_event(1, "allow"),
        make_event(2, "low_confidence"),
        make_event(3, "allow"),
    ]
    summary = dashboard.build_summary(events)
    assert summary["total_events"] == 3
    assert summary["outcome_counts"]["allow"] == 2
    assert summary["outcome_counts"]["low_confidence"] == 1
    assert len(summary["alerts"]) == 1


def test_dashboard_markdown_renders_table():
    events = [make_event(1, "allow")]
    summary = dashboard.build_summary(events)
    md = dashboard.render_markdown(summary)
    assert "# Single-Save Decision Telemetry Summary" in md
    assert "| allow | 1 |" in md
    assert "No active alerts." in md
