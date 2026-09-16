import uuid
import json
import pytest

# Simple in-memory mocks to simulate the policy/harness

def decision_policy(per_model_scores, impact_level, audit_ref):
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
    # But ensure audit content is verifiable (in real system verify signature)
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
    cmd, outcome = decision_policy(scores, 'high', audit_ref='evidence/manifest.json')
    assert cmd is None
    assert outcome == 'requires_approval'


def test_allows_actuation_with_confidence_and_audit():
    scores = make_scores(0.95)
    cmd, outcome = decision_policy(scores, 'low', audit_ref='evidence/manifest.json')
    assert cmd is not None
    assert outcome == 'allow'
    assert 'decision_id' in cmd

# Run with: pytest .copilot-tracking/rai-plans/negotiate-with-kaiju/single-save-decision/tests -q
