"""In-memory telemetry emitter for the Single-Save Decision Layer 5 harness.

Emits structured decision events matching the schema in
`layer5-telemetry-harness.md`. This in-memory sink stands in for the real
publish-to-`logs/inference/central/` pipeline (see RAI backlog item
{{RAI-TEMP-4}}). Each event carries a monotonically increasing `sequence`
number as an anti-replay control per T-RAI-006.
"""
import datetime


class TelemetryEmitter:
    def __init__(self):
        self._events = []
        self._sequence = 0

    def emit(self, decision_id, outcome, aggregated_confidence, impact_level, audit_ref):
        self._sequence += 1
        event = {
            "sequence": self._sequence,
            "decision_id": decision_id,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "aggregated_confidence": aggregated_confidence,
            "decision": outcome,
            "impact_level": impact_level,
            "audit_ref": audit_ref,
        }
        self._events.append(event)
        return event

    @property
    def events(self):
        return list(self._events)
