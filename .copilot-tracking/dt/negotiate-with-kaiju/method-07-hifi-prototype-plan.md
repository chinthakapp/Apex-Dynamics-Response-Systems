# Method 07 — High-Fidelity Prototype Plan

Project: Negotiate with Kaiju
Date: 2026-09-15

Purpose: Detail a production-like prototype for the most promising concept, including integration, testing, and acceptance criteria.


Selected concept: Pulsed Light Modulation (primary)

Key components (assumed specs)
- Stimulus module: 8x high-intensity programmable LED array, PWM control, max 1200 lm per cluster, optical diffusers to avoid human-eye hazard.
- Control gateway: hardened Raspberry Pi-class edge device with signed command channel, hardware kill-switch for immediate shutdown, NTP-synced RTC.
- Evidence stack: 3x synchronized cameras (primary, flank, overview), local MinIO gateway for immediate upload, SHA256 manifest generator.
- Safety: physical perimeter fencing, remote abort button, Safety Officer console with two-step confirm.

Timeline (assumed)
- Week 0: procure LED array, edge hardware, cameras.
- Week 1: bench integration and verification; run smoke-test scripts and evidence pipeline validation.
- Week 2: controlled environment validation run and acceptance sign-off.

Acceptance criteria (assumed)
- System triggers and abort execute within 200ms of command.
- Evidence manifests uploaded and checksums verified within T+60s of run completion.
- Behavioral metrics replicate lo-fi success thresholds (>=40% reduction in aggression markers during stimulus window).

Operational responsibilities (assumed)
- Field Lead: device ops and safety interlock control.
- Safety Officer: final abort authority and go/no-go sign-off.
- Data Lead: evidence ingestion, checksum verification, and manifest registration.


Integration checklist
- Hardware mounts and safety cages.
- Encrypted control channel and two-step abort.
- Full logging: device logs, operator inputs, timestamps.

Acceptance criteria
- Prototype operates for full trial duration without critical failure.
- Evidence manifests show intact checksums and server receipts.
- Behavioral metrics meet or exceed lo-fi success thresholds.

Deployment notes
- Prepare maintenance and spare parts list.
- Schedule staged validation in a controlled environment prior to field trial.
