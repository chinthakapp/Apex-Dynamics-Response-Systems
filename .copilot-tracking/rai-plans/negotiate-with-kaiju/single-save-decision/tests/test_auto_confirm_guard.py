import uuid
import json
import pytest

from .mocks.mock_minio import MockMinIO

# Simple in-memory mocks to simulate the policy/harness

def decision_policy(per_model_scores, impact_level, audit_ref, minio: MockMinIO = None):
    """Simplified decision policy for tests.
    Returns emitted_command or None and decision outcome string.
    """
    aggregated_confidence = sum(per_model_scores)/len(per_model_scores)
    CONFIDENCE_THRESHOLD = 0.9
    if impact_level == 'high':
        return None, 'requires_approval'
    if audit_ref is None:
        return None, 'requires_audit'
    if aggregated_confidence < CONFIDENCE_THRESHOLD:
        return None, 'low_confidence'
    # At this point audit_ref present and confidence high
    # verify audit exists in MinIO mock if provided
    if minio is not None:
        obj = minio.get_object('evidence', audit_ref)
        if obj is None:
            return None, 'missing_audit_record'
    # Allow actuation
    return {'command': 'actuate', 'decision_id': str(uuid.uuid4())}, 'allow'


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

# Run with: pytest .copilot-tracking/rai-plans/negotiate-with-kaiju/single-save-decision/tests -q
