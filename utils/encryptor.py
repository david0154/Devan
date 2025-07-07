from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

कुञ्जिका = b'संस्कृतसुरक्षा॥॥'  # AES कञ्जिका (16 वर्णानि)

def सङ्केतय(पाठः: str) -> bytes:
    यन्त्रः = AES.new(कुञ्जिका, AES.MODE_CBC)
    संकेतितम् = यन्त्रः.encrypt(pad(पाठः.encode(), AES.block_size))
    print("🔐 सङ्केतनं सम्पूर्णम्।")
    return यन्त्रः.iv + संकेतितम्

def विसङ्केतय(डाटा: bytes) -> str:
    आरम्भः = डाटा[:16]
    यन्त्रः = AES.new(कुञ्जिका, AES.MODE_CBC, आरम्भः)
    मूलम् = unpad(यन्त्रः.decrypt(डाटा[16:]), AES.block_size)
    print("📜 विसङ्केतनं सम्पूर्णम्।")
    return मूलम्.decode()
