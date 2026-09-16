# Layer 4 — Verification Spec

Objective: Define tests and harness that verify the decision policy never auto-confirms a life-safety actuation without required signals.

Key invariants (must hold)
- INV-1: No auto-actuation without `confidence` >= `CONFIDENCE_THRESHOLD` and `audit_ref` present.
- INV-2: Any `impact_level` == `high` requires explicit `approval` records (two-person) — auto-actuation disallowed.
- INV-3: For each decision, a signed `audit_record` (JSON) must be persisted and referencable by `decision_id`.

Test types
- Unit tests: decision policy function with mocked inputs (simulate low/high confidence, missing audit, tampered audit).
- Integration tests: end-to-end flow from mocked sensor inputs to decision output and audit persistence (MinIO mock).
- Property tests: randomized inputs asserting invariants hold for a wide range of inputs.

Test harness architecture
- `tests/` directory with `mocks/`: `mock_actuator`, `mock_minio`, `mock_approval_service`.
- Use `pytest` with fixtures to inject mocks and capture emitted commands (no real actuator calls).

Sample test (pseudocode)
- GIVEN ensemble outputs with aggregated confidence=0.95 and audit_ref=None
- WHEN decision_policy evaluates
- THEN assert that `emitted_command` == `null` and `decision_outcome` == `requires_approval`

Acceptance: All INV-* tests green in CI before enabling auto-actuation in staging.
