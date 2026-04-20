from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256
import base64

class SecureEncryptor:
    def __init__(self, secret_key: str):
        self.key = sha256(secret_key.encode()).digest()

    def encrypt(self, data: str) -> str:
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct = cipher.encrypt(pad(data.encode(), AES.block_size))
        return base64.b64encode(cipher.iv + ct).decode()

    def decrypt(self, enc: str) -> str:
        raw = base64.b64decode(enc)
        iv = raw[:16]
        ct = raw[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size).decode()
