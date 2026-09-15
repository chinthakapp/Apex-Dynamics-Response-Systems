#!/usr/bin/env python3
"""Evidence ingest smoke-test
Usage: python method-02-evidence-smoke-test.py --file sample.mp4 --endpoint https://ingest.example/api/upload

This script computes SHA256 of the given file and POSTs it to the ingest endpoint with metadata.
"""
import argparse
import hashlib
import json
import os
import requests
import sys


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--file", required=True, help="Local file to upload")
    p.add_argument("--endpoint", required=True, help="Ingest endpoint URL")
    p.add_argument("--api-key", required=False, help="API key for ingest (optional)")
    args = p.parse_args()

    if not os.path.exists(args.file):
        print("File not found:", args.file)
        sys.exit(2)

    checksum = sha256_file(args.file)
    size = os.path.getsize(args.file)
    metadata = {
        "filename": os.path.basename(args.file),
        "sha256": checksum,
        "size": size,
        "utc_ts": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "trial_id": "light-trial-01",
    }

    files = {"file": open(args.file, "rb")}
    data = {"metadata": json.dumps(metadata)}
    headers = {}
    if args.api_key:
        headers["Authorization"] = f"Bearer {args.api_key}"

    print("Uploading to", args.endpoint)
    r = requests.post(args.endpoint, files=files, data=data, headers=headers, timeout=30)
    print("Status:", r.status_code)
    try:
        print("Response:", r.json())
    except Exception:
        print("Response text:", r.text)


if __name__ == "__main__":
    main()
