# Security Backlog (GitHub format) — negotiate-with-kaiju

Below are handoff-ready GitHub issue drafts. IDs use the temporary template `{{SEC-TEMP-N}}`. Autonomy tier: `partial` (agent drafts, human approves).

---
{{SEC-TEMP-1}} Title: Harden MinIO ingestion and enable immutable storage
Priority: High
Description: Enable TLS on MinIO endpoints, enforce object-lock (WORM) for evidence buckets, restrict access to service account with least privilege, rotate access keys.
Acceptance Criteria:
- MinIO TLS enabled and verified.
- Evidence bucket has object lock/WORM enabled.
- Service account credentials rotated and documented.
- Access control policy reviewed and applied.
Owner: infra
Autonomy: partial

---
{{SEC-TEMP-2}} Title: Implement manifest signing and verification for all evidence bundles
Priority: Critical
Description: Add a signing step that produces an authenticated manifest (SHA256 + signature) for each trial bundle; ingestion scripts must verify signature before acceptance.
Acceptance Criteria:
- Signing keypair created and stored in secure keystore.
- `method-02-evidence-smoke-test.py` verifies signatures and rejects unsigned bundles.
- Documentation added to repository with verification steps.
Owner: platform
Autonomy: partial

---
{{SEC-TEMP-3}} Title: Enforce operator MFA and RBAC for console and packet generation
Priority: High
Description: Require MFA for all operator console accounts and restrict `generate-packet.ps1` execution to a privileged role; add separation of duties for Safety Officer.
Acceptance Criteria:
- MFA enabled for all operator accounts.
- Role definitions and RBAC policies implemented.
- `generate-packet.ps1` callable only by authorized role.
Owner: ops
Autonomy: partial

---
{{SEC-TEMP-4}} Title: Sanitize and sandbox `generate-packet.ps1` execution
Priority: High
Description: Validate inputs to packet generator, run generator in ephemeral container or restricted account, and ensure no network egress except to MinIO.
Acceptance Criteria:
- Input validation implemented.
- Generator runs inside sandboxed environment.
- No unexpected network egress during generation.
Owner: platform
Autonomy: partial

---
{{SEC-TEMP-5}} Title: Protect device-to-cloud channels (TLS, anti-replay)
Priority: High
Description: Ensure telemetry channels use mutual TLS or TLS+HMAC, implement sequence numbers/timestamps to prevent replay, and monitor for anomalies.
Acceptance Criteria:
- TLS or mTLS enabled for telemetry.
- Replay protection implemented.
- Anomaly alerts configured.
Owner: infra
Autonomy: partial

---
{{SEC-TEMP-6}} Title: Implement tamper-evident logging and central audit collector
Priority: High
Description: Centralize logs, enable append-only storage, NTP-sync hosts, and ensure log retention for forensic investigation.
Acceptance Criteria:
- Central log collector configured.
- Logs are time-synced and append-only.
- Retention policy documented.
Owner: security
Autonomy: partial

---
{{SEC-TEMP-7}} Title: Threat detection rules for suspicious telemetry patterns
Priority: Medium
Description: Create detection rules for telemetry anomalies (replay, sudden coordinate jumps, sensor spoofing) and integrate into alerting dashboard.
Acceptance Criteria:
- Rule set implemented and tested against synthetic anomalies.
- Alerts routed to on-call with runbooks.
Owner: security
Autonomy: partial

---
{{SEC-TEMP-8}} Title: Ensure controlled abort authority and measure abort latency
Priority: Critical
Description: Codify Safety Officer abort workflow, implement secure abort channel, and run latency testing to verify abort response ≤ 200 ms in hi‑fi environment.
Acceptance Criteria:
- Abort workflow documented and approved.
- Abort channel authenticated and secured.
- Latency test results recorded and acceptable.
Owner: safety
Autonomy: manual

---
{{SEC-TEMP-9}} Title: Dependency and supply-chain scanning for ingestion and packet generator scripts
Priority: Medium
Description: Scan Python/PowerShell dependencies, add SBOM, and require signed releases for third-party libs used in evidence pipeline.
Acceptance Criteria:
- SBOM generated and stored.
- Vulnerability scan results triaged.
- Approved dependency list maintained.
Owner: platform
Autonomy: partial

---
{{SEC-TEMP-10}} Title: Access review and credential rotation playbook
Priority: Medium
Description: Establish regular access reviews for operator and service accounts and an automated rotation schedule for keys used by field controllers and MinIO.
Acceptance Criteria:
- Playbook documented.
- Rotation automation implemented or scheduled.
- Recent access review completed.
Owner: ops
Autonomy: partial
