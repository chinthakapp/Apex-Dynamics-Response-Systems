"""Plain-text/markdown dashboard summary for Single-Save Decision telemetry.

Renders a human-readable report from telemetry events plus any evaluated
alerts, intended for a non-technical stakeholder view (console, Slack
message, or a markdown snippet embedded in a status page). Not a live
dashboard service -- see RAI backlog {{RAI-TEMP-4}} for the real ingestion
and visualization pipeline.
"""
from collections import Counter
import importlib.util
import pathlib

_spec = importlib.util.spec_from_file_location(
    "alerting", str(pathlib.Path(__file__).parent / "alerting.py")
)
_alerting = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_alerting)
evaluate_alerts = _alerting.evaluate_alerts


def build_summary(events):
    """Return a dict with counts-by-outcome and the active alert list."""
    outcome_counts = Counter(event.get("decision") for event in events)
    alerts = evaluate_alerts(events)
    return {
        "total_events": len(events),
        "outcome_counts": dict(outcome_counts),
        "alerts": alerts,
    }


def render_markdown(summary):
    """Render `build_summary()` output as a small markdown report."""
    lines = ["# Single-Save Decision Telemetry Summary", ""]
    lines.append(f"Total decisions observed: {summary['total_events']}")
    lines.append("")
    lines.append("| Outcome | Count |")
    lines.append("|---------|-------|")
    for outcome, count in sorted(summary["outcome_counts"].items(), key=lambda kv: kv[0] or ""):
        lines.append(f"| {outcome} | {count} |")
    lines.append("")
    if summary["alerts"]:
        lines.append("## Active Alerts")
        lines.append("")
        lines.append("| Severity | Decision ID | Reason |")
        lines.append("|----------|-------------|--------|")
        for alert in summary["alerts"]:
            lines.append(f"| {alert['severity']} | {alert['decision_id']} | {alert['reason']} |")
    else:
        lines.append("No active alerts.")
    return "\n".join(lines)
