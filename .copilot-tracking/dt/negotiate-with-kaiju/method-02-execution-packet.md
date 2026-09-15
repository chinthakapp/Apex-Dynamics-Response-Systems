# Method 02 — Execution Packet (Printable)

Project: Negotiate with Kaiju — light-trial-01
Dry-run: 2026-09-16 10:00 PT
Live trial: 2026-09-17 10:00 PT (pending sign-off)
Staging (approx): 47.809000, -122.121513

1) Contacts
- Trial Coordinator: [Name] — coordinator@placeholder.example
- Operator: Tim Cook — operator@placeholder.example
- Safety Officer: [Name] — safety@placeholder.example
- Comms Lead: [Name] — comms@placeholder.example
- Evidence Lead: [Name] — evidence@placeholder.example

2) Approvals
- Safety Officer signed: __________  Date: __________
- Permit attached: __________  Reference: __________

3) Equipment List (on-site)
- Main stimulus device (serial): __________
- Backup stimulus device (serial): __________
- Video recorders (x3) — make/model/serial: __________
- NTP gateway device: __________
- Evidence gateway/minio node: __________
- SAT phone: +1-555-0100
- Backup radio: 145.500 MHz

4) Evidence Capture Protocol
- Start recordings and note UTC start time.
- Generate SHA256 checksums locally; add to `manifest.json`.
- Upload to ingest endpoint; confirm signed receipt.
- Save local copies to external drive and to MinIO.

5) Dry-run Script (T-120m → T+10m)
- T-120m: power on devices, confirm NTP sync, test ingest upload.
- T-60m: safety briefing and perimeter check.
- T-30m: operator walk-through of ramp and abort sequence.
- T-10m: final evidence-ingest smoke test.
- 0: start 60s pulsed sequence (1 Hz) with conservative ramp.
- T+10s: observer notes.
- T+60s: shutdown and immediate evidence upload verification.

6) Abort Procedure
- Abort phrase: "ABORT TRIAL NOW" — Safety Officer confirms verbally and via SAT phone.
- Operator executes immediate hardware interlock shutdown and records action in chain-of-custody log.

7) Post-trial
- Observers sign witness statements and attach to evidence packet.
- Evidence lead verifies checksums and timestamps; record results in `manifest.json`.
- Produce quick incident report and upload to `.copilot-tracking/dt/negotiate-with-kaiju/evidence/{trial-id}/report.pdf`.

8) Attachments (to include when printing)
- `method-02-trial-plan.md` (full parameters)
- `method-02-observation-checklist.md`
- `method-02-approval-one-pager.md`
- `method-02-consent-form.md`

Signed off by: ____________________  Date: __________
