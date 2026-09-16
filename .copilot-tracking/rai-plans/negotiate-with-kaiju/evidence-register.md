# Phase 5 — Evidence Register

Purpose: Record where evidence resides, collection method, chain-of-custody notes, and tamper-evidence controls.

1. Signed Dataset Manifests
- Location: `.copilot-tracking/rai-plans/negotiate-with-kaiju/evidence/signed-datasets/`
- Collected by: ML Engineering CI (post-ingest signing via cosign)
- Chain-of-Custody: CI job produces manifest, cosigned, uploaded to MinIO with object-lock
- Tamper Controls: cosign verification, MinIO object-lock, replication to cold backup

2. Model Training CI Logs
- Location: `artifacts/ci/training/`
- Collected by: CI pipeline
- Chain-of-Custody: retained in CI artifact storage, checksummed, backed up
- Tamper Controls: access controls, immutability policies

3. Sensor Validation and Firmware Signatures
- Location: `infrastructure/sensors/firmware/` and `data/`
- Collected by: Field Ops during provisioning
- Chain-of-Custody: provisioning ticket + signed firmware record
- Tamper Controls: hardware attestation, secure boot

4. Inference-Time Anomaly Logs
- Location: `logs/inference/` (edge) -> replicated to `logs/inference/central/`
- Collected by: runtime monitoring agent
- Chain-of-Custody: agent pushes signed batches with sequence numbers
- Tamper Controls: TLS + mTLS for push, sequence numbers, retention

5. Approval Workflow Records (Actuation)
- Location: `workflows/approvals/`
- Collected by: human-in-the-loop approval service
- Chain-of-Custody: each approval signed by operator creds, stored with timestamp
- Tamper Controls: WORM, access logging, MFA enforced

6. MinIO Configuration and Replication Logs
- Location: MinIO admin console (exported to `infra/minio/`)
- Collected by: Infrastructure automation
- Chain-of-Custody: infra-as-code commits generate config; replication snapshots pushed to cold-storage
- Tamper Controls: TLS, RBAC, object-lock, external backup

7. SBOMs and Build Signatures
- Location: `artifacts/sbom/` and `artifacts/signatures/`
- Collected by: CI builds
- Chain-of-Custody: CI signs build artifacts; SBOM attached to release
- Tamper Controls: signature verification during deploy

8. Telemetry Redaction Reports
- Location: `data/telemetry/redaction/`
- Collected by: ingest pipeline
- Chain-of-Custody: redaction job logs with checksums
- Tamper Controls: access logs, audit trail

Metadata fields for register entries:
- id: unique evidence id (e.g., EVID-001)
- description
- path
- collector
- collection_date
- chain_of_custody
- verification_method
- retention_policy
- tamper_controls
- responsible_owner

Next steps: create the `evidence/` folder under the plan, start exporting CI artifacts into `evidence/`, and team must verify access policies before enabling auto-collection.
