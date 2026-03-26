import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from app.config import settings


def _get_key() -> bytes:
    return bytes.fromhex(settings.ENCRYPT_MASTER_KEY)


def encrypt_api_key(plaintext: str) -> str:
    """AES-256-GCM 加密 API Key，返回 base64 密文"""
    key = _get_key()
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)
    ct = aesgcm.encrypt(nonce, plaintext.encode(), None)
    return base64.b64encode(nonce + ct).decode()


def decrypt_api_key(ciphertext: str) -> str:
    """解密 API Key，返回明文（仅在内存中使用，不落日志）"""
    key = _get_key()
    data = base64.b64decode(ciphertext)
    nonce, ct = data[:12], data[12:]
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ct, None).decode()
