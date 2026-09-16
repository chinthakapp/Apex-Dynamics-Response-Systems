import uuid
import json
import pytest

import importlib.util
import pathlib

# load helper modules from tests/mocks without requiring package imports
tests_dir = pathlib.Path(__file__).parent


def _load(module_name, filename):
    spec = importlib.util.spec_from_file_location(module_name, str(tests_dir / "mocks" / filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


MockMinIO = _load("mock_minio", "mock_minio.py").MockMinIO
_signing = _load("evidence_signing", "evidence_signing.py")
verify_signature = _signing.verify_signature
sign_manifest = _signing.sign_manifest
TelemetryEmitter = _load("telemetry", "telemetry.py").TelemetryEmitter

SIGNING_KEY = b"test-signing-key"

# Simple in-memory mocks to simulate the policy/harness

def decision_policy(per_model_scores, impact_level, audit_ref, minio: MockMinIO = None,
                     signing_key: bytes = None, telemetry: TelemetryEmitter = None):
    """Simplified decision policy for tests.
    Returns emitted_command or None and decision outcome string.
    """
    aggregated_confidence = sum(per_model_scores)/len(per_model_scores)
    CONFIDENCE_THRESHOLD = 0.9

    def _finish(command, outcome):
        if telemetry is not None:
            decision_id = command.get('decision_id') if command else None
            telemetry.emit(decision_id, outcome, aggregated_confidence, impact_level, audit_ref)
        return command, outcome

    if impact_level == 'high':
        return _finish(None, 'requires_approval')
    if audit_ref is None:
        return _finish(None, 'requires_audit')
    if aggregated_confidence < CONFIDENCE_THRESHOLD:
        return _finish(None, 'low_confidence')
    # At this point audit_ref present and confidence high
    # verify audit exists in MinIO mock if provided
    if minio is not None:
        obj = minio.get_object('evidence', audit_ref)
        if obj is None:
            return _finish(None, 'missing_audit_record')
        if signing_key is not None:
            signature = obj.get('metadata', {}).get('signature')
            if not signature or not verify_signature(obj['data'], signature, signing_key):
                return _finish(None, 'invalid_audit_signature')
    # Allow actuation
    return _finish({'command': 'actuate', 'decision_id': str(uuid.uuid4())}, 'allow')


def make_scores(val, n=3):
    return [val]*n


def test_no_auto_actuation_without_audit():
    scores = make_scores(0.95)
    cmd, outcome = decision_policy(scores, 'medium', audit_ref=None)
    assert cmd is None
    assert outcome in ('requires_audit','requires_approval') or outcome == 'requires_audit'


def test_no_auto_actuation_for_high_impact_even_with_audit():
    scores = make_scores(0.99)
    cmd, outcome = decision_policy(scores, 'high', audit_ref='manifest.json')
    assert cmd is None
    assert outcome == 'requires_approval'


def test_allows_actuation_with_confidence_and_audit_present():
    minio = MockMinIO()
    # create audit object
    minio.put_object('evidence', 'manifest.json', b'{"decision": "signed"}')
    scores = make_scores(0.95)
    cmd, outcome = decision_policy(scores, 'low', audit_ref='manifest.json', minio=minio)
    assert cmd is not None
    assert outcome == 'allow'
    assert 'decision_id' in cmd


def test_blocks_when_audit_missing_in_minio():
    minio = MockMinIO()
    scores = make_scores(0.95)
    cmd, outcome = decision_policy(scores, 'low', audit_ref='manifest.json', minio=minio)
    assert cmd is None
    assert outcome == 'missing_audit_record'


def test_allows_actuation_with_valid_signature():
    minio = MockMinIO()
    data = b'{"decision": "signed"}'
    signature = sign_manifest(data, SIGNING_KEY)
    minio.put_object('evidence', 'manifest.json', data, metadata={'signature': signature})
    scores = make_scores(0.95)
    cmd, outcome = decision_policy(scores, 'low', audit_ref='manifest.json', minio=minio, signing_key=SIGNING_KEY)
    assert cmd is not None
    assert outcome == 'allow'


def test_blocks_when_audit_signature_invalid():
    minio = MockMinIO()
    data = b'{"decision": "signed"}'
    minio.put_object('evidence', 'manifest.json', data, metadata={'signature': 'not-a-valid-signature'})
    scores = make_scores(0.95)
    cmd, outcome = decision_policy(scores, 'low', audit_ref='manifest.json', minio=minio, signing_key=SIGNING_KEY)
    assert cmd is None
    assert outcome == 'invalid_audit_signature'


def test_blocks_when_audit_signature_missing():
    minio = MockMinIO()
    data = b'{"decision": "signed"}'
    minio.put_object('evidence', 'manifest.json', data)
    scores = make_scores(0.95)
    cmd, outcome = decision_policy(scores, 'low', audit_ref='manifest.json', minio=minio, signing_key=SIGNING_KEY)
    assert cmd is None
    assert outcome == 'invalid_audit_signature'


def test_telemetry_emits_event_per_decision_with_increasing_sequence():
    telemetry = TelemetryEmitter()
    minio = MockMinIO()
    data = b'{"decision": "signed"}'
    minio.put_object('evidence', 'manifest.json', data, metadata={'signature': sign_manifest(data, SIGNING_KEY)})
    scores = make_scores(0.95)

    decision_policy(scores, 'medium', audit_ref=None, telemetry=telemetry)
    decision_policy(scores, 'low', audit_ref='manifest.json', minio=minio, signing_key=SIGNING_KEY, telemetry=telemetry)

    assert len(telemetry.events) == 2
    assert telemetry.events[0]['sequence'] == 1
    assert telemetry.events[1]['sequence'] == 2
    assert telemetry.events[0]['decision'] == 'requires_audit'
    assert telemetry.events[1]['decision'] == 'allow'

# Run with: pytest .copilot-tracking/rai-plans/negotiate-with-kaiju/single-save-decision/tests -q
