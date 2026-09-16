"""Alert rule evaluation for Single-Save Decision telemetry events.

Implements the "Monitoring & Alerts" rules from `layer5-telemetry-harness.md`:
- Alert on any decision outcome that indicates a missing or invalid audit trail.
- Alert on low-confidence outcomes (potential model degradation).
- Alert on repeated high-confidence `allow` decisions within a short window
  across distinct decision_ids (possible poisoning / replay), per T-RAI-006.

Consumes the event list produced by `telemetry.TelemetryEmitter` (or any
list of dicts with the same schema). No live monitoring stack required;
this is a pure function suitable for wiring into a real alerting backend
(PagerDuty, Slack webhook, etc.) later (RAI backlog {{RAI-TEMP-4}}).
"""

ALERT_OUTCOMES = {
    "missing_audit_record": "critical",
    "invalid_audit_signature": "critical",
    "low_confidence": "warning",
}

# Number of consecutive high-confidence 'allow' events within this many
# sequence positions that triggers a possible-poisoning alert.
REPEATED_ALLOW_WINDOW = 3
REPEATED_ALLOW_THRESHOLD = 3


def evaluate_alerts(events):
    """Return a list of alert dicts: {sequence, decision_id, severity, reason}."""
    alerts = []

    for event in events:
        outcome = event.get("decision")
        if outcome in ALERT_OUTCOMES:
            alerts.append({
                "sequence": event["sequence"],
                "decision_id": event.get("decision_id"),
                "severity": ALERT_OUTCOMES[outcome],
                "reason": f"decision outcome '{outcome}' requires attention",
            })

    allow_events = [e for e in events if e.get("decision") == "allow"]
    for i in range(len(allow_events) - REPEATED_ALLOW_THRESHOLD + 1):
        window = allow_events[i:i + REPEATED_ALLOW_THRESHOLD]
        sequences = [e["sequence"] for e in window]
        if max(sequences) - min(sequences) < REPEATED_ALLOW_WINDOW + REPEATED_ALLOW_THRESHOLD:
            alerts.append({
                "sequence": window[-1]["sequence"],
                "decision_id": window[-1].get("decision_id"),
                "severity": "warning",
                "reason": (
                    f"{REPEATED_ALLOW_THRESHOLD} 'allow' decisions within a short window "
                    "(possible poisoning/replay per T-RAI-006)"
                ),
            })

    return alerts
