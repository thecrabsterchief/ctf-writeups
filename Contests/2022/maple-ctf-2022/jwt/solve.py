from jwt import ES256

from fastecdsa.curve import secp256k1
from base64 import urlsafe_b64decode
from hashlib import sha256
from Crypto.Util.number import bytes_to_long as bl

n = secp256k1.q

def b64decode(msg: str) -> bytes:
    if len(msg) % 4 != 0:
        msg += "=" * (4 - len(msg) % 4)
    return urlsafe_b64decode(msg.encode())

def recover_private_key(token):
    header, data, signature = token.split(".")
    signature = b64decode(signature)

    # s*d = z + r*d  [mod n]
    z = bl(sha256((header + "." + data).encode()).digest())
    r, s = [
        int.from_bytes(signature[:32], "little"), 
        int.from_bytes(signature[32:], "little")
    ]
    d = z * pow(s - r, -1, n) % n
    return d


if __name__ == "__main__":
    jwt = ES256()
    
    token = jwt.sign({"user" : "hacker"})
    d     = recover_private_key(token)
    print("[+] Recovered private key:", d)

    admin_token = ES256(private=d).sign({"user" : "admin"})
    print("[+] Signing an admin token:", token)

    assert jwt.decode(admin_token)