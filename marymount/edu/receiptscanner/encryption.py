
import base64
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class AESCipher:
    def __init__(self, secret: str):
        # 256-bit key
        self.key = sha256(secret.encode()).digest()

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
