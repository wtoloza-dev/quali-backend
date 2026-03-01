"""Simple Fernet encryption for sensitive fields like document numbers."""

from cryptography.fernet import Fernet

from app.core.settings import settings


def _get_fernet() -> Fernet:
    key = settings.ENCRYPTION_KEY
    if not key:
        raise RuntimeError("ENCRYPTION_KEY is not configured.")
    return Fernet(key.encode())


def encrypt(value: str) -> str:
    """Encrypt a plaintext string. Returns base64-encoded ciphertext."""
    return _get_fernet().encrypt(value.encode()).decode()


def decrypt(value: str) -> str:
    """Decrypt a base64-encoded ciphertext. Returns plaintext."""
    return _get_fernet().decrypt(value.encode()).decode()
