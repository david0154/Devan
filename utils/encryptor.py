from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256

# 🔑 AES कञ्जिका (derived from a Sanskrit phrase)
कुञ्जिका = sha256('संस्कृतसुरक्षा॥॥'.encode('utf-8')).digest()[:16]

def सङ्केतय(पाठः: str) -> bytes:
    यन्त्रः = AES.new(कुञ्जिका, AES.MODE_CBC)
    संकेतितम् = यन्त्रः.encrypt(pad(पाठः.encode('utf-8'), AES.block_size))
    print("🔐 सङ्केतनं सम्पूर्णम्।")
    return यन्त्रः.iv + संकेतितम्

def विसङ्केतय(डाटा: bytes) -> str:
    आरम्भः = डाटा[:16]
    यन्त्रः = AES.new(कुञ्जिका, AES.MODE_CBC, आरम्भः)
    मूलम् = unpad(यन्त्रः.decrypt(डाटा[16:]), AES.block_size)
    print("📜 विसङ्केतनं सम्पूर्णम्।")
    return मूलम्.decode('utf-8')

<<<<<<< HEAD
# 🧠 Aliases for import in devan_runner.py
encrypt = सङ्केतय
decrypt = विसङ्केतय

# 🧪 Example usage
if __name__ == "__main__":
    सन्देशः = "नमस्ते जगत्"
    सङ्केतितम् = encrypt(सन्देशः)
    प्रतिफलम् = decrypt(सङ्केतितम्)
=======
# उदाहरनम् (Example)
if __name__ == "__main__":
    सन्देशः = "नमस्ते जगत्"
    सङ्केतितम् = सङ्केतय(सन्देशः)
    प्रतिफलम् = विसङ्केतय(सङ्केतितम्)
>>>>>>> 10b93076c1cb298208de5f8bcefd42bd2eb6971c
    print("🔏 मूलपाठः:", प्रतिफलम्)
