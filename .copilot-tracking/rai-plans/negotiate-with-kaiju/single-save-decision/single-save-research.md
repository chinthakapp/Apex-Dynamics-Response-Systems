# Single-Save Decision — Research

Scope: harden the prototype "Single-Save Decision" (edge decision that may trigger life-safety actuation) into a governed feature with verification and telemetry.

Objectives
- Prevent any autonomous actuation that affects human life unless a confidence threshold and a signed audit record exist.
- Provide reproducible tests (Layer 4 verification) and telemetry/audit (Layer 5) for incident review and forensics.

Assumptions
- Decision input sources: multi-sensor fusion (radar, lidar, camera), operator override channel, ensemble model outputs.
- Actuation channels support signed command envelopes and two-person approval for high-impact actions.
- Evidence store: MinIO with object-lock available for artifact retention.

Decision Path (summary)
1. Sensors -> preprocessing -> fused observation
2. Inference ensemble -> per-model confidence scores
3. Decision policy: compute action recommendations and an aggregated confidence
4. If aggregated confidence >= SAFE_THRESHOLD AND audit record exists AND action impact_level != "high" -> allow auto-actuation
5. If impact_level == "high" -> require two-person approval regardless of confidence

Data & Evidence sources
- `data/sensor-grid.txt` ingestion logs
- CI-signed training manifests
- inference logs: `logs/inference/`
- approval workflow records: `workflows/approvals/`

Gaps Identified
- No implemented test harness to assert audit-record enforcement.
- Telemetry schema needs fields for `confidence`, `decision_id`, `audit_ref`, `operator_ids`, `impact_level`, `timestamp`, `signature`.

Next: translate verification goals into Layer 4 test specs and Layer 5 telemetry schema.
