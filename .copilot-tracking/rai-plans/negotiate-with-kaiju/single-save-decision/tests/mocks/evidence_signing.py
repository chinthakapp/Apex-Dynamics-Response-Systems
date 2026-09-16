"""Evidence manifest signing/verification.

This is a lightweight stand-in for cosign/sigstore signing so the decision
policy can verify audit manifests without requiring the cosign binary or a
live Sigstore/Fulcio/Rekor deployment in this environment. Swap
`sign_manifest`/`verify_signature` for real cosign verify-blob calls before
production use (see RAI backlog item {{RAI-TEMP-2}}).
"""
import hashlib
import hmac


def sign_manifest(data: bytes, key: bytes) -> str:
    """Return a hex HMAC-SHA256 signature for the given manifest bytes."""
    return hmac.new(key, data, hashlib.sha256).hexdigest()


def verify_signature(data: bytes, signature: str, key: bytes) -> bool:
    """Verify a manifest signature produced by `sign_manifest`."""
    expected = sign_manifest(data, key)
    return hmac.compare_digest(expected, signature)
