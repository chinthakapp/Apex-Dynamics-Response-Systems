# Security Plan — negotiate-with-kaiju

## Scope (Phase 1 summary)
- Project slug: `negotiate-with-kaiju`
- Entry mode: `capture` (scoping defaults accepted)
- Deployment targets: `edge-devices`, `field-controllers`, `cloud/minio`, `operator-workstations` (assumed)
- Data classification: `internal` (sensor telemetry, trial metadata, video/images, manifests, logs)
- Autonomy tier: `partial` (agent drafts, human approves)
- RAI: none detected / `raiEnabled: false`

## Operational Buckets
- Infrastructure: field controllers, network switches, NTP, power
- DevOps / Platform: CI, build scripts, `generate-packet.ps1`, ingestion scripts
- Build: packaging, artifact signing, dependency management
- Messaging: sensor telemetry channels, MQTT/HTTP endpoints, MinIO ingestion
- Data: sensor logs, video/images, manifests, SHA256 bundles
- Web/UI/Reporting: operator consoles, dashboards, PDF packets
- Identity/Auth: operator accounts, device credentials, MinIO access keys
- Governance & Security (cross-cutting): safety officer, abort controls, audit logging

## System Boundaries and Trust Model
- Prompts / Commands: operator inputs, `generate-packet.ps1` parameters — trust level: human-operator (high)
- Data Inputs: sensor telemetry, device heartbeats, manifests — trust level: medium (unsigned by default)
- Tools: ingestion scripts (`method-02-evidence-smoke-test.py`), packet generator — execution environment must be trusted
- Outputs: PDF packets, alert messages, operator console state — must be integrity-protected

## Threat Model (high-level)
Key threats mapped to STRIDE categories:
- T-INF-001 (Tamper): sensor data tampering or replay to conceal or fake Kaiju behavior — Impact: High
- T-AUTH-002 (Spoofing): unauthorized device or operator forging telemetry or commands — Impact: Critical
- T-AV-003 (Availability): DDoS or resource exhaustion of field controllers or MinIO ingestion — Impact: High
- T-INFO-004 (Information Disclosure): leakage of sensitive images, location metadata, or internal comms — Impact: Medium
- T-EXEC-005 (Elevation/Malicious Output): malicious or malformed `generate-packet.ps1` causing operator deception — Impact: High
- T-LOG-006 (Insufficient Logging): missing tamper-evident audit trail for trials — Impact: High

## Controls Mapping (summary)
Note: full standards mapping available on request; this is a prioritized control set mapped to OWASP/NIST/CIS.

- Identity & Access (Auth): enforce RBAC, short-lived credentials, MFA for operator accounts
  - OWASP: A1 (Broken Access Control)
  - NIST SP 800-53: AC-2, AC-3, IA-2
  - CIS Controls v8: 4 (Secure Config), 6 (Access Control)

- Data Integrity & Transport: TLS for telemetry, signed manifests (SHA256 + signature), anti-replay (nonces/TIMESTAMP+HMAC)
  - OWASP: A02 (Cryptographic Failures)
  - NIST: SC-8, SC-13, SI-7
  - CIS: 16 (Account Monitoring) and 14 (Secure Config for network)

- Device & Build Hardening: secure boot where possible, artifact signing, dependency scanning
  - OWASP: A05 (Security Misconfiguration)
  - NIST: CM-2, SI-2
  - CIS: 1 (Inventory), 2 (Vulnerability Management), 11 (Secure Config)

- Input Validation & Execution Safety: sanitize operator inputs to `generate-packet.ps1`, validate manifests, run generator in sandbox/readonly workspace
  - OWASP: A03 (Injection)
  - NIST: SI-10
  - CIS: 8 (Audit Logging), 18 (Application Software Security)

- Logging & Forensics: append-only, time-synced logs, immutable evidence storage (MinIO with object lock), SHA256 manifests stored separate from raw data
  - OWASP: A10 (Insufficient Logging)
  - NIST: AU-2, AU-6
  - CIS: 6 (Access Control), 8 (Audit Log Management)

- Resilience & Safety Controls: safety officer abort authority, hardware kill-switch procedures, misfire/abort latency tests (target ≤ 200 ms)
  - NIST: CP-10 (Information System Recovery and Reconstitution)

## Residual Risks
- Human operator compromise remains a high residual risk; prioritize MFA and separation of duties.
- Field device physical compromise is possible — treat high-impact sensors as untrusted until evidence-signed.

## Next Actions (recommended)
1. Harden MinIO: enable TLS, object-lock (WORM), strong keys, rotate credentials.
2. Add manifest signing: generate keypair, sign SHA256 manifests; publish public key in repo PKI store.
3. Harden `generate-packet.ps1` and ingestion scripts: input validation, run under restricted service account.
4. Implement tamper-evident logging and central audit collector.
5. Run controlled smoke-test and record outcomes; validate abort latency with Safety Officer present.

## Artifacts
- `.copilot-tracking/dt/negotiate-with-kaiju/PRD.md`
- `.copilot-tracking/dt/negotiate-with-kaiju/diagrams.md`
- `.copilot-tracking/dt/negotiate-with-kaiju/method-02-evidence-smoke-test.py`
