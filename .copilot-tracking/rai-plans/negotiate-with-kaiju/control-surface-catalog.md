# Phase 5 — Control Surface Catalog

Purpose: Map identified RAI threats to existing and recommended controls, owners, and evidence sources.

Threat → Controls → Owner → Evidence

T-RAI-001 (Data Poisoning)
- Controls: signed datasets, dataset provenance, training pipeline CI gating, data vetting scripts
- Owner: ML Engineering
- Evidence: `.copilot-tracking/rai-plans/negotiate-with-kaiju/system-definition-pack.md`, model training CI logs, signed dataset manifests (cosign)
- Priority: High

T-RAI-002 (Adversarial Sensor Spoofing)
- Controls: sensor redundancy, cross-sensor consistency checks, sensor crypto/signing, plausibility filters
- Owner: Field Engineering / Sensor Ops
- Evidence: sensor validation test outputs, sensor firmware signatures, `data/sensor-grid.txt` ingest logs
- Priority: High

T-RAI-003 (Model Evasion)
- Controls: input sanitization, ensemble checks, runtime detection, adversarial robustness tests
- Owner: ML Engineering
- Evidence: adversarial test harness reports, inference-time anomaly logs
- Priority: High

T-RAI-004 (Prompt Injection / Recommender Manipulation)
- Controls: prompt/context sanitization, allowlist of high-impact actions, offline policy review, signed upstream inputs
- Owner: Platform / Security
- Evidence: request sanitization logs, LLM context provenance, CI policy review artifacts
- Priority: High

T-RAI-005 (Actuator Tampering / Unauthorized Commands)
- Controls: authenticated command channels (mTLS), signed firmware, hardware attestation, two-person approval for high-impact commands
- Owner: Field Ops / Security
- Evidence: firmware signatures, attestation logs, approval workflow records
- Priority: Critical

T-RAI-006 (Output Manipulation / Replay Attacks)
- Controls: anti-replay (nonces/sequence numbers), TTL for commands, signed command envelopes
- Owner: Platform / Field Ops
- Evidence: network command logs with sequence numbers, crypto envelopes
- Priority: High

T-RAI-007 (Evidence Store Tampering)
- Controls: MinIO TLS, object-lock/WORM, immutable backups, remote replication, strict RBAC
- Owner: Security / Infrastructure
- Evidence: MinIO configuration, retention policies, replication logs
- Priority: High

T-RAI-008 (Supply-Chain / Artifact Tampering)
- Controls: cosign/sigstore signing, SBOMs, CI verification gates, limited build access
- Owner: DevOps / Security
- Evidence: SBOMs, cosign signatures in CI, build logs
- Priority: High

T-RAI-009 (Privacy Leakage)
- Controls: PII scanning at ingest, redaction/anonymization pipeline, RBAC for telemetry
- Owner: Data Governance
- Evidence: PII scan reports, redaction logs
- Priority: Medium

T-RAI-010 (Model Stealing)
- Controls: rate limiting, output truncation, watermarking, monitoring for extraction patterns
- Owner: Platform / Security
- Evidence: API access logs, monitoring alerts for extraction patterns
- Priority: Medium

Notes: Controls marked "Existing" are present in the security plan; others are recommended. Next: map each control to implementation tasks and evidence collection steps in the `evidence-register.md`.
