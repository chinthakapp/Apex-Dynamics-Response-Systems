# Product Requirements Document — Negotiate with Kaiju

Status: Draft (assumed outcomes per user instruction)
Date: 2026-09-15

## 1. Purpose

Provide a clear, auditable PRD for the `negotiate-with-kaiju` Design Thinking project. The goal is to design, prototype, and validate a safe, non-lethal intervention (primary: Pulsed Light decoy) to divert Kaiju attention away from populated areas and gather forensic-grade evidence for future prevention and negotiation.

All research outcomes, test results, and experiment observations in this PRD are *assumed* per the user instruction to skip live interviews and trials. Live verification and Safety Officer sign-off remain mandatory before any field activity.

## 2. Objectives
- Avoid Kaiju attacks on the city by diverting attention to a decoy or non-harmful stimulus.
- Reduce measured aggression/attack probability by at least 40–50% in controlled trials.
- Capture forensic-grade evidence (NTP-synced, SHA256 manifests) for each trial.
- Produce reproducible execution artifacts: trial plan, evidence manifests, packet PDF, and deployment roadmap.

## 3. Scope

In Scope:
- Design & validation of Pulsed Light decoy and mobile decoy concepts.
- Evidence pipeline: ingestion, SHA256 manifests, local + S3-compatible backup at `.copilot-tracking/dt/negotiate-with-kaiju/evidence/{trial-id}/`.
- Lo-fi → hi-fi prototype plans, test protocol, and iteration roadmap.

Out of Scope:
- Live deployments without Safety Officer & regulatory approvals.
- Any lethal or harmful countermeasures.

## 4. Stakeholders
- Project Lead / Design Lead: (assumed)
- Safety Officer: has unilateral abort authority (abort phrase: "ABORT TRIAL NOW").
- Evidence Custodian: responsible for manifests, checksums, and MinIO uploads.
- Field Ops: responsible for staging coordinates and physical setup.

## 5. Key Assumptions
- User directed to skip interviews and live actions; Methods 2–9 populated with assumed results.
- Geolocation: conservative staging coordinates used (47.809000, -122.121513).
- Trial `light-trial-01` parameters: 1 Hz pulsed light, 60 s duration, ramp 0→100% over 5 s.
- Evidence pipeline dependencies installed as described in project artifacts (Python `requests` required for ingestion scripts).

## 6. Success Metrics & Acceptance Criteria
- Functional: average aggression reduction ≥ 40% across 5 trial runs (assumed result: ~48%).
- Technical: evidence manifests present and SHA256 checksums verify for every captured artifact.
- Safety: abort response time ≤ 200 ms in hi-fi acceptance tests.
- Documentation: trial plan, smoke-test script, evidence manifests, and packet PDF available and reproducible from artifacts.

Acceptance Criteria (done):
- `method-02-trial-plan.md`, `method-02-evidence-smoke-test.py`, and `method-08-results.md` exist in `.copilot-tracking/dt/negotiate-with-kaiju/`.
- All artifacts are recorded in `coaching-state.md` with timestamps and the canonical workflow opt-in noted.

## 7. Trial Summary (light-trial-01)
- Stimulus: Pulsed Light (primary), mobile decoy (secondary).
- Parameters: 1 Hz pulse, 60 s active window, 5 s conservative ramp.
- Safety Controls: two-step abort, Safety Officer authority, hardware kill-switch.
- Evidence: each trial produces a SHA256 manifest file (`manifest-trial-01.sha256`, etc.) and raw capture artifacts placed under the evidence folder.

## 8. Evidence & Integrity
- Devices must be NTP-synced before trial start.
- Each captured file must be hashed (SHA256) and recorded in a manifest alongside timestamps.
- Redundant storage strategy: local and MinIO (S3-compatible) backup path `.copilot-tracking/dt/negotiate-with-kaiju/evidence/{trial-id}/`.

## 9. Deliverables
- Trial plan: `method-02-trial-plan.md` (existing).
- Smoke-test script: `method-02-evidence-smoke-test.py` (existing).
- Execution packet generator: `generate-packet.ps1` (existing) — used to produce PDF packet.
- PRD (this file).
- Test results: `method-08-results.md` (existing, assumed data).
- Iteration roadmap: `method-09-iteration-roadmap.md` (existing).

## 10. Timeline & Milestones (provisional)
- Week 0: Documentation, Safety Officer sign-off, and permits.
- Week 1: Lo-fi trials and evidence smoke-test (assumed completed).
- Week 2: Hi-fi prototyping and acceptance testing.
- Week 3+: Iterations and staged rollout per `method-09-iteration-roadmap.md`.

## 11. Risks & Mitigations
- Risk: Assumed results may not replicate in live trials. Mitigation: mandate small incremental tests with Safety Officer oversight.
- Risk: Evidence chain breaks (clock drift, missing manifests). Mitigation: enforce NTP sync and automated manifest verification prior to storage.
- Risk: Public safety/regulatory restrictions. Mitigation: obtain permits and community notifications before any field activity.

## 12. Next Steps
1. Confirm that you want the PRD stored in `.copilot-tracking/dt/negotiate-with-kaiju/PRD.md` (created) — or move to `docs/prd/` for tracked checkout.
2. If desired, I can run `generate-packet.ps1` to produce the execution PDF now.
3. If you want this added to Git history, I'll add & commit the file (force-add if required).

---
Notes:
- This PRD is intentionally explicit that outcomes are assumed; live verification and Safety Officer approvals remain required before any operational steps.
