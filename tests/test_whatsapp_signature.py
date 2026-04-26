"""Unit tests for HMAC X-Hub-Signature-256 verification on the WhatsApp webhook."""
import hashlib
import hmac

from app.services.whatsapp_sender import verify_signature


def _sign(body: bytes, secret: str) -> str:
    return "sha256=" + hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()


def test_valid_signature_accepted():
    body = b'{"foo":"bar"}'
    sig = _sign(body, "test-secret")
    assert verify_signature(body, sig, "test-secret") is True


def test_wrong_secret_rejected():
    body = b'{"foo":"bar"}'
    sig = _sign(body, "different-secret")
    assert verify_signature(body, sig, "test-secret") is False


def test_tampered_body_rejected():
    body = b'{"foo":"bar"}'
    sig = _sign(body, "test-secret")
    tampered = b'{"foo":"baz"}'
    assert verify_signature(tampered, sig, "test-secret") is False


def test_missing_signature_header_rejected():
    body = b'{"foo":"bar"}'
    assert verify_signature(body, "", "test-secret") is False


def test_missing_secret_rejected():
    body = b'{"foo":"bar"}'
    sig = _sign(body, "test-secret")
    assert verify_signature(body, sig, "") is False


def test_wrong_algorithm_prefix_rejected():
    body = b'{"foo":"bar"}'
    assert verify_signature(body, "md5=abc123", "test-secret") is False


def test_empty_body_with_correct_signature():
    body = b''
    sig = _sign(body, "test-secret")
    assert verify_signature(body, sig, "test-secret") is True
