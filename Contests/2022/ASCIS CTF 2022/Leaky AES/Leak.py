from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto import Random

flag = open("flag.txt", "rb").read()
nonce = Random.get_random_bytes(8)
countf = Counter.new(64, nonce)
key = Random.get_random_bytes(32)

encrypto = AES.new(key, AES.MODE_CTR, counter=countf)
encrypted = encrypto.encrypt(b"TODO:\n - ADD HARDER CHALLENGE IN CRYPTO\n - ADD FLAG TO THE CHALLENGE\n")

encrypto = AES.new(key, AES.MODE_CTR, counter=countf)
encrypted2 = encrypto.encrypt(flag)

print(f"encrypted: {encrypted}")
print(f"encrypted2: {encrypted2}")

# encrypted: b"\xb3y\xf5Ky\xed\x13\xcd\x85U1\xbb\x9c\xd8?A\xe9?P/\xc3/\x97\x97\xbf\xe3\xfam\xb9\x00\xf0_\xf3\x02s\x97\x1b\x87\xeb\t\xda\xe6\x04@0\x9a\xa8\xea\x8b\xa9\x86\x87\x1c-\xeaDI\x8b\xd1v\x1e6!\xc8'\x06_\xd4\xb9"

# encrypted2: b'\xa6e\xf2M\x10\x9cp\x8f\xcbs\x07\x9e\xc8\xe5\x12r\xd9\x1f]n\xee\x03\x89\x8c\xc0\xca\xd7\x1a\x91E\xe6e\xe3\x1e`\x9d\x02\x80\xfb@\xa8\x92tUD\x81\xeb\xc4\xa6\x84\xad\xda'
