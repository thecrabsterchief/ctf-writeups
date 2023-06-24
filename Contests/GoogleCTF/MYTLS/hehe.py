import binascii
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import hmac
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import hashlib
import os
from secrets import token_hex

key = open("./server-ecdhkey.pem", "r").read()
with open("./log1.txt", "w+") as f:
    for i in range(len(key)):
        f.write(hashlib.sha256(b"1"*i + key[i:].encode()).hexdigest() + "\n")