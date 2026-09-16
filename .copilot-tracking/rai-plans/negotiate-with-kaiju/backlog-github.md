<!-- markdownlint-disable-file -->
# RAI Backlog — GitHub Issue Templates (Negotiate-with-Kaiju / Single-Save Decision)

Autonomy tier: Partial (default per instructions — draft items for human review before creation; none created automatically).

---

## {{RAI-TEMP-1}}: Wire production MinIO with object-lock (WORM) for evidence store

```yaml
---
rai_characteristic: Secure and Resilient
threat_id: T-RAI-007
suggested_priority: Near-term
suggested_horizon: Pre-Production
category: Control Implementation
depth_tier: Standard
security_cross_ref: WI-SEC-007
---
```

## RAI Control: Evidence store immutability

**NIST Characteristic:** Secure and Resilient
**Threat:** T-RAI-007 - Evidence Store Tampering
**Control Surface:** prevent - Replace `MockMinIO` with a real MinIO deployment configured with TLS, object-lock/WORM, and strict RBAC
**Suggested Priority:** Near-term
**Suggested Remediation Horizon:** Pre-Production

### Implementation

Deploy MinIO (or equivalent S3-compatible store) with object-lock enabled in compliance mode for the `evidence` bucket. Update `decision_policy()` integration to call the real client instead of the in-memory mock used in `test_auto_confirm_guard.py`.

### Acceptance Criteria

* [ ] Real MinIO client wired behind the same interface as `MockMinIO`
* [ ] Object-lock/WORM verified via integration test
* [ ] Retention policy documented in `evidence-register.md`

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-2}}: Add cosign signature verification to audit records

```yaml
---
rai_characteristic: Accountable and Transparent
threat_id: T-RAI-008
suggested_priority: Near-term
suggested_horizon: Pre-Production
category: Control Implementation
depth_tier: Standard
security_cross_ref: WI-SEC-008
---
```

## RAI Control: Signed audit records

**NIST Characteristic:** Accountable and Transparent
**Threat:** T-RAI-008 - Supply-Chain / Artifact Tampering
**Control Surface:** detect - Verify cosign signatures on audit manifests before `decision_policy()` treats an `audit_ref` as valid
**Suggested Priority:** Near-term
**Suggested Remediation Horizon:** Pre-Production

### Implementation

Extend `decision_policy()` to call a signature-verification step against the object retrieved from the evidence store, rejecting unsigned or invalid manifests with a new `invalid_audit_signature` outcome.

### Acceptance Criteria

* [x] Signature verification function added and unit tested (HMAC-SHA256 stand-in at `tests/mocks/evidence_signing.py`)
* [x] New `invalid_audit_signature` outcome covered by a test case
* [ ] Verification failure path logged to telemetry
* [ ] Replace HMAC stand-in with real cosign/Sigstore verify-blob call before production

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-3}}: Run Single-Save Decision CI on the main repository

```yaml
---
rai_characteristic: Valid and Reliable
threat_id: T-RAI-003
suggested_priority: Near-term
suggested_horizon: Pre-Production
category: Monitoring Setup
depth_tier: Standard
security_cross_ref: ''
---
```

## RAI Control: Continuous verification of the auto-confirm guard

**NIST Characteristic:** Valid and Reliable
**Threat:** T-RAI-003 - Model Evasion
**Control Surface:** detect - `.github/workflows/ci-single-save.yml` runs `pytest` against the Single-Save Decision tests on push/PR
**Suggested Priority:** Near-term
**Suggested Remediation Horizon:** Pre-Production

### Implementation

The workflow is committed but has not executed on the origin repository because push access is unavailable to the current account (`chinthakapp`). Options: (1) grant collaborator access, (2) merge from the fork `chinthakapp/Apex-Dynamics-Response-Systems` (branch `main`), or (3) re-add the workflow directly on `AmieDD/Apex-Dynamics-Response-Systems`.

### Acceptance Criteria

* [ ] Workflow executes successfully on the target repository's default branch
* [ ] CI status badge added to `README.md`

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-4}}: Telemetry ingestion pipeline for Layer 5 harness

```yaml
---
rai_characteristic: Accountable and Transparent
threat_id: T-RAI-006
suggested_priority: Planned
suggested_horizon: Early Operations
category: Monitoring Setup
depth_tier: Standard
security_cross_ref: WI-SEC-006
---
```

## RAI Control: Decision telemetry pipeline

**NIST Characteristic:** Accountable and Transparent
**Threat:** T-RAI-006 - Output Manipulation / Replay Attacks
**Control Surface:** detect - Implement the ingestion pipeline described in `layer5-telemetry-harness.md`, forwarding `decision_id`, outcome, confidence, and audit_ref to a monitored sink
**Suggested Priority:** Planned
**Suggested Remediation Horizon:** Early Operations

### Implementation

Build the collector described in the Layer 5 spec; add anti-replay sequence numbers to emitted events per T-RAI-006 mitigation.

### Acceptance Criteria

* [x] Telemetry events emitted for every `decision_policy()` outcome (in-memory `TelemetryEmitter` at `tests/mocks/telemetry.py`)
* [x] Anti-replay sequence numbers present on each event
* [ ] Dashboard or alert rule for `missing_audit_record` and `low_confidence` outcomes
* [ ] Replace in-memory sink with real publish path to `logs/inference/central/` over mTLS

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-5}}: PII scanning and redaction for telemetry

```yaml
---
rai_characteristic: Privacy-Enhanced
threat_id: T-RAI-009
suggested_priority: Planned
suggested_horizon: Early Operations
category: Control Implementation
depth_tier: Standard
security_cross_ref: WI-SEC-009
---
```

## RAI Control: Telemetry privacy filter

**NIST Characteristic:** Privacy-Enhanced
**Threat:** T-RAI-009 - Privacy Leakage
**Control Surface:** prevent - Add a PII scan/redaction step before telemetry events are persisted or forwarded
**Suggested Priority:** Planned
**Suggested Remediation Horizon:** Early Operations

### Implementation

Introduce a redaction pass keyed off known PII field patterns (names, coordinates tied to individuals) prior to writing telemetry to durable storage.

### Acceptance Criteria

* [ ] Redaction pipeline covers all telemetry event fields
* [ ] Redaction verified with sample PII fixtures in tests

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-6}}: Explainability surrogate for confidence scoring

```yaml
---
rai_characteristic: Explainable and Interpretable
threat_id: ''
suggested_priority: Backlog
suggested_horizon: Ongoing Governance
category: Enhancement
depth_tier: Standard
security_cross_ref: ''
---
```

## RAI Control: Interpretable surrogate model

**NIST Characteristic:** Explainable and Interpretable
**Threat:** N/A — enhancement, not a direct threat mitigation
**Control Surface:** n/a - Provide a simplified, interpretable surrogate (e.g., decision-tree approximation) alongside the per-model confidence ensemble to support human review of `allow`/`requires_approval` outcomes
**Suggested Priority:** Backlog
**Suggested Remediation Horizon:** Ongoing Governance

### Implementation

Train a surrogate model against historical decision outcomes; surface top contributing factors alongside each `decision_id` in the audit trail.

### Acceptance Criteria

* [ ] Surrogate model produces a top-factors explanation for each decision
* [ ] Explanation stored alongside the audit record

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-7}}: Bias evaluation for per-model confidence scoring

```yaml
---
rai_characteristic: Fair with Harmful Bias Managed
threat_id: ''
suggested_priority: Backlog
suggested_horizon: Ongoing Governance
category: Enhancement
depth_tier: Standard
security_cross_ref: ''
---
```

## RAI Control: Confidence-scoring bias review

**NIST Characteristic:** Fair with Harmful Bias Managed
**Threat:** N/A — enhancement, not a direct threat mitigation
**Control Surface:** n/a - Evaluate `per_model_scores` aggregation for systematic bias across scenario types (city zones, population density) before production rollout
**Suggested Priority:** Backlog
**Suggested Remediation Horizon:** Ongoing Governance

### Implementation

Run the aggregation logic against a stratified test set spanning representative scenario categories; document any disparate confidence patterns and mitigations.

### Acceptance Criteria

* [ ] Bias evaluation report produced across at least 3 scenario categories
* [ ] Mitigation plan documented for any disparity found

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-8}}: Document transparency note for Single-Save Decision

```yaml
---
rai_characteristic: Accountable and Transparent
threat_id: ''
suggested_priority: Backlog
suggested_horizon: Ongoing Governance
category: Documentation
depth_tier: Standard
security_cross_ref: ''
---
```

## RAI Control: Transparency documentation

**NIST Characteristic:** Accountable and Transparent
**Threat:** N/A — documentation gap
**Control Surface:** n/a - Publish a transparency note covering system purpose, capabilities, limitations, and human-oversight points for the Single-Save Decision feature
**Suggested Priority:** Backlog
**Suggested Remediation Horizon:** Ongoing Governance

### Implementation

Use the Transparency Note Outline template from the RAI backlog-handoff instructions; populate with details from `single-save-research.md` and `single-save-plan.md`.

### Acceptance Criteria

* [ ] Transparency note drafted and reviewed by stakeholders
* [ ] Linked from `README.md` or project documentation index

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-9}}: Merge or grant access for Single-Save Decision branch

```yaml
---
rai_characteristic: Accountable and Transparent
threat_id: ''
suggested_priority: Immediate
suggested_horizon: Pre-Production
category: Remediation
depth_tier: Standard
security_cross_ref: ''
---
```

## RAI Control: Repository access remediation

**NIST Characteristic:** Accountable and Transparent
**Threat:** N/A — process/access gap, not a system threat
**Control Surface:** n/a - The account used for this session (`chinthakapp`) lacks push/PR-creation rights on `AmieDD/Apex-Dynamics-Response-Systems`. All commits are pushed to `chinthakapp/Apex-Dynamics-Response-Systems` (fork, branch `main`, commit `6a4eb1c`) pending manual merge.
**Suggested Priority:** Immediate
**Suggested Remediation Horizon:** Pre-Production

### Implementation

Repository owner should either grant collaborator access to `chinthakapp` and re-run `git push origin main`, or manually merge from the fork using the compare URL: `https://github.com/AmieDD/Apex-Dynamics-Response-Systems/compare/main...chinthakapp:Apex-Dynamics-Response-Systems:main`.

### Acceptance Criteria

* [ ] Commits `8f0e33a`..`6a4eb1c` present on `AmieDD/Apex-Dynamics-Response-Systems` main branch
* [ ] CI workflow executes on the target repository

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer
