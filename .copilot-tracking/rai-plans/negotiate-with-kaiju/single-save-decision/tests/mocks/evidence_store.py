"""Production evidence store backed by MinIO with object-lock (WORM) support.

Implements the same conceptual interface as `mocks/mock_minio.MockMinIO`
(`put_object`, `get_object`, `list_objects`) plus `ensure_bucket` for
object-lock-enabled bucket provisioning, satisfying RAI backlog item
{{RAI-TEMP-1}}.

Requires a running MinIO (or S3-compatible, object-lock-capable) endpoint.
Configure via environment variables or constructor arguments:
  MINIO_ENDPOINT       e.g. "minio.internal:9000"
  MINIO_ACCESS_KEY
  MINIO_SECRET_KEY
  MINIO_SECURE         "true"/"false" (default "true")
  MINIO_EVIDENCE_BUCKET (default "evidence")

This module is not used by the local pytest suite (which uses MockMinIO to
avoid requiring live infrastructure). It is provided so the real
integration is a drop-in swap once a MinIO endpoint is available -- see
`test_evidence_store.py` for API-contract tests using a mocked `Minio`
client (no network required).
"""
import io
import os
from datetime import datetime, timedelta, timezone

from minio import Minio
from minio.commonconfig import GOVERNANCE
from minio.error import S3Error
from minio.retention import Retention


class MinIOEvidenceStore:
    def __init__(self, endpoint=None, access_key=None, secret_key=None,
                 secure=None, bucket=None, client=None):
        self.bucket = bucket or os.environ.get("MINIO_EVIDENCE_BUCKET", "evidence")
        if client is not None:
            self.client = client
        else:
            self.client = Minio(
                endpoint or os.environ["MINIO_ENDPOINT"],
                access_key=access_key or os.environ["MINIO_ACCESS_KEY"],
                secret_key=secret_key or os.environ["MINIO_SECRET_KEY"],
                secure=secure if secure is not None else
                os.environ.get("MINIO_SECURE", "true").lower() == "true",
            )

    def ensure_bucket(self):
        """Create the evidence bucket with object-lock enabled if it does not exist."""
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket, object_lock=True)

    def put_object(self, object_name, data: bytes, metadata=None, retention_days=365):
        """Upload an evidence object under GOVERNANCE-mode object-lock retention."""
        retain_until = datetime.now(timezone.utc) + timedelta(days=retention_days)
        retention = Retention(GOVERNANCE, retain_until)
        return self.client.put_object(
            self.bucket,
            object_name,
            io.BytesIO(data),
            length=len(data),
            metadata=metadata,
            retention=retention,
            legal_hold=False,
        )

    def get_object(self, object_name):
        """Return {'data': bytes, 'metadata': dict} or None if the object does not exist."""
        try:
            response = self.client.get_object(self.bucket, object_name)
            data = response.read()
            response.close()
            response.release_conn()
        except S3Error as exc:
            if exc.code == "NoSuchKey":
                return None
            raise
        stat = self.client.stat_object(self.bucket, object_name)
        return {"data": data, "metadata": dict(stat.metadata or {})}

    def list_objects(self, prefix=None):
        return [obj.object_name for obj in self.client.list_objects(self.bucket, prefix=prefix)]
