# Single-Save Decision — Implementation Plan

Goal: Move prototype to governed feature with verification (Layer 4) and telemetry/audit (Layer 5).

Deliverables
- `layer4-verification-spec.md` — concrete tests and harness design
- `layer5-telemetry-harness.md` — telemetry schema and ingestion plan
- `tests/test_auto_confirm_guard.py` — pytest harness asserting no auto-confirm without confidence and audit
- Evidence exports to `single-save-decision/evidence/`

Acceptance Criteria
- Automated tests that fail if the system would auto-actuate without a confidence score or audit record.
- Telemetry includes required audit fields and is persisted to MinIO with object-lock.
- Two-person approval enforced for high-impact actions.

Milestones
1. Research (done) -> 2 days review with stakeholders
2. Layer 4 spec -> implement unit and integration tests (3 days)
3. Layer 5 schema & ingestion -> deploy telemetry stubs to staging (2 days)
4. Run verification, collect evidence, update `evidence-register.md` (1 day)
5. Produce Phase 6 handoff backlog (1 day)

Risks & Mitigations
- Running tests against live actuators: use mock actuators and sandboxed staging environment.
- Evidence replication lag: snapshot evidence immediately at decision time.

Owners
- ML Engineering: tests and model confidence metrics
- Platform/Security: audit record schema, signing, MinIO config
- Field Ops: approval workflows and hardware gating

Next: create Layer 4 spec and Layer 5 telemetry harness.
