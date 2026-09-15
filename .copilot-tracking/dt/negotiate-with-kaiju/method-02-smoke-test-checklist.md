# Evidence Ingest Smoke-test Checklist

Purpose: verify evidence ingest endpoint, checksum verification, and receipt generation before dry-run.

Prerequisites
- Python 3.8+ and `requests` installed (`pip install -r requirements.txt`).
- A small sample file (e.g., `sample.mp4`) to upload.
- Ingest endpoint URL and API key (if required).

Steps
1. Ensure NTP sync on the test machine: `w32tm /query /status` (Windows) or `timedatectl status` (Linux).
2. Compute local SHA256 and store in `manifest-local.json`:
   - `python method-02-evidence-smoke-test.py --file sample.mp4 --endpoint https://ingest.example/api/upload --api-key YOUR_KEY`
3. Verify HTTP 200/201 response and that the response contains a server-verified checksum or receipt.
4. Confirm the server checksum matches the local SHA256; if mismatch, stop and investigate.
5. Repeat with a second device to ensure redundant upload works.

Success Criteria
- Server returns a signed receipt or identical checksum.
- Upload completes within 120s for the sample file.
- Ingest logs show `trial_id: light-trial-01` and operator info.

If failures occur, capture logs and abort the dry-run until resolved.
