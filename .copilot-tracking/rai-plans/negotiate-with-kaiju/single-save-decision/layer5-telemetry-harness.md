# Layer 5 — Telemetry & Audit Harness

Telemetry schema (decision event)
- `decision_id`: string (UUID)
- `timestamp`: ISO8601
- `inputs`: short digest of observation sources
- `per_model_scores`: map[string,float]
- `aggregated_confidence`: float
- `decision`: string (e.g., `allow`, `require_approval`, `deny`)
- `impact_level`: enum(`low`,`medium`,`high`)
- `audit_ref`: string (object path or manifest id)
- `operator_ids`: array[string] (if approval)
- `signatures`: { `issuer`, `signature` }

Ingestion plan
- Edge agent publishes signed decision events to `logs/inference/central/` over mTLS.
- Each decision event includes a minimal audit JSON uploaded to MinIO `single-save-decision/evidence/` with object-lock and a cosign-like signature.

Audit record structure
- `decision_id`, `decision_inputs_hash`, `per_model_scores`, `aggregated_confidence`, `policy_version`, `created_by` (service id), `approvals` (array of approval objects), `signature`

Retention & Forensics
- Retain full audit records for incident window 365 days; long-term cold storage for confirmed incidents.
- Immediate snapshot: upon any `decision` where `impact_level` != `low`, snapshot raw sensor frames to `evidence/` bucket with signed manifest.

Monitoring & Alerts
- Alert on any inference event missing `audit_ref` but reporting `decision` != `deny`.
- Alert on repeated high-confidence changes across short windows (possible poisoning).

Next: implement mock MinIO and pytest harness under `tests/` as described in Layer 4.
