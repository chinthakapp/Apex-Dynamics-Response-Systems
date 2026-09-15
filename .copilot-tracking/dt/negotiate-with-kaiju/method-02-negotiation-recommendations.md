# Method 02 — Assumptions & Recommendations (Skip-to-Action)

Project: Negotiate with Kaiju
Date: 2026-09-15

Purpose: Apply reasonable operational assumptions and industry best-practice recommendations so the team can proceed immediately with a dry-run and evidence-capture trial without repeating earlier DT steps.

Assumptions (accepted unless you change them)
- Staging coordinate: 47.809000, -122.121513 (approx. Walmart Redmond fallback).
- Test datetime: 2026-09-16 10:00 PT (dry-run), live trial: 2026-09-17 10:00 PT.
- Operator: Tim Cook (operator@placeholder.example). Safety Officer: [Name] (safety@placeholder.example).
- Comms primary: SAT phone +1-555-0100; backup: Radio freq 145.500 MHz.
- Abort phrase standardized to: "ABORT TRIAL NOW" (requires Safety Officer two-step confirmation).
- Device requirements: NTP-synced, generate SHA256 checksums, upload to ingest endpoint within 120s of capture.

Minimum Required Approvals (before live trial)
- Safety Officer signed `method-02-approval-one-pager.md`.
- Local permits verified and attached to the packet.
- Evidence ingest endpoint test pass and checksum verification success.

Operational Recommendations
- Dry-run (T-120m) checklist: full ramp/shutdown, evidence upload test, abort path test with simulated abort, operator rehearsal.
- Evidence retention: keep raw and processed copies; manifest: `evidence/{trial-id}/manifest.json` with checksums and timestamps.
- Communications: open voice channel on SAT phone and backup radio during trial; assign a comms lead.
- Observer roles: two independent observers to sign witness statements immediately after trial.
- Safety: maintain 300m safe perimeter; no public presence inside 500m unless authorized.

Data Integrity & Security
- All devices record UTC timestamps; ingest API verifies SHA256 on upload and returns a signed receipt stored in metadata.
- Local gateway produces an HMAC-signed upload manifest to MinIO; metadata mirrored to Postgres.
- Chain-of-custody: each evidence file appended to `evidence/{trial-id}/chain-of-custody.log` with operator signature and timestamp.

Quick Decision Rules (for on-site operator)
- If Kaiju shows increased aggression within 10s of stimulus ramp, trigger immediate abort and escalate to Safety Officer.
- If network/ingest fails, hold evidence locally and retry; abort only on safety criteria, not for temporary comms loss.

Next Immediate Actions (I will do these if you confirm)
1. Produce printable `method-02-execution-packet.md` and a PDF-ready version.
2. Create calendar invites for the dry-run and four interviews using `method-02-interview-schedule.md` placeholders.
3. Run an evidence-ingest smoke test (I will produce the test script and upload checklist).

Approve these assumptions as-is, or tell me which to change. If approved, reply "Proceed" and I'll generate the execution packet and calendar invites.
