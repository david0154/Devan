from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

KEY = b'SanskritLangKey!!'  # 16 bytes key

def encrypt(data: str) -> bytes:
    cipher = AES.new(KEY, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    return cipher.iv + ct_bytes

def decrypt(data: bytes) -> str:
    iv = data[:16]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(data[16:]), AES.block_size)
    return pt.decode()
