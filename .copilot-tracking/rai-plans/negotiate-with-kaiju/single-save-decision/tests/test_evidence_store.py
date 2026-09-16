"""API-contract tests for MinIOEvidenceStore using a mocked minio.Minio client.

No network or live MinIO server is required: `client` is injected as a
MagicMock configured to mimic the minio SDK's return shapes.
"""
import io
from unittest.mock import MagicMock

import importlib.util
import pathlib

from minio.commonconfig import GOVERNANCE
from minio.error import S3Error

tests_dir = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location(
    "evidence_store", str(tests_dir / "mocks" / "evidence_store.py")
)
evidence_store_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evidence_store_mod)
MinIOEvidenceStore = evidence_store_mod.MinIOEvidenceStore


def make_store():
    client = MagicMock()
    store = MinIOEvidenceStore(bucket="evidence", client=client)
    return store, client


def test_ensure_bucket_creates_with_object_lock_when_missing():
    store, client = make_store()
    client.bucket_exists.return_value = False

    store.ensure_bucket()

    client.make_bucket.assert_called_once_with("evidence", object_lock=True)


def test_ensure_bucket_skips_creation_when_present():
    store, client = make_store()
    client.bucket_exists.return_value = True

    store.ensure_bucket()

    client.make_bucket.assert_not_called()


def test_put_object_applies_governance_retention():
    store, client = make_store()

    store.put_object("manifest.json", b'{"decision": "signed"}', retention_days=365)

    assert client.put_object.call_count == 1
    _, kwargs = client.put_object.call_args
    assert kwargs["retention"].mode == GOVERNANCE
    assert kwargs["legal_hold"] is False


def test_get_object_returns_data_and_metadata_on_success():
    store, client = make_store()
    response = MagicMock()
    response.read.return_value = b'{"decision": "signed"}'
    client.get_object.return_value = response
    stat = MagicMock()
    stat.metadata = {"signature": "abc123"}
    client.stat_object.return_value = stat

    result = store.get_object("manifest.json")

    assert result == {"data": b'{"decision": "signed"}', "metadata": {"signature": "abc123"}}


def test_get_object_returns_none_when_missing():
    store, client = make_store()
    client.get_object.side_effect = S3Error(
        response=None, code="NoSuchKey", message="not found",
        resource="/evidence/manifest.json", request_id="r", host_id="h",
    )

    result = store.get_object("manifest.json")

    assert result is None


def test_list_objects_returns_names():
    store, client = make_store()
    obj_a = MagicMock(object_name="manifest-a.json")
    obj_b = MagicMock(object_name="manifest-b.json")
    client.list_objects.return_value = [obj_a, obj_b]

    result = store.list_objects()

    assert result == ["manifest-a.json", "manifest-b.json"]
