#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode
from Crypto.Util.Padding import pad
import string

try:
    FLAG = open("flag", "rb").read()        # flag is here! 
except:
    FLAG = b'[**FLAG**]'

class AES_Cipher:
    def __init__(self):
        self.key = get_random_bytes(16)
    def encrypt(self, data: bytes):
        cipher = AES.new(self.key, AES.MODE_CBC)
        self.iv = b64encode(cipher.iv).decode('utf-8')
        self.cipher_t = b64encode(cipher.encrypt(pad(data, AES.block_size))).decode('utf-8')
        return 'AES_iv: ' + self.iv + '\nAES_cipher_text: ' + self.cipher_t

class RSA_Cipher:
    def __init__(self):
        self.e = 65537
        self.n = 13119132709177697801
    def encrypt(self, data: int):
        cipher_n = pow(data, self.e, self.n)
        return cipher_n

class Caesar_Cipher:
    def __init__(self):
        self.alpha = list(string.ascii_lowercase)
    def encrypt(self, data: str): 
        cipher_t = [i for i in range(len(data))]
        for i in range(len(data)):
            ch = data[i]
            if(ch in self.alpha):
                idx = self.alpha.index(ch)
                cipher_t[i] = self.alpha[(idx + 13) % 26]
            else:
                cipher_t[i] = ch
        return ''.join(cipher_t)


ac = AES_Cipher()
rc = RSA_Cipher()
cc = Caesar_Cipher()

ac_key = int.from_bytes(ac.key, 'big')

# Key 1
rc_p = hex(ac_key)[2:16]
rc_c = rc.encrypt(int(rc_p, 16))
print('Key1:', hex(rc_c)[2:])

# Key 2
cc_p = hex(ac_key)[16:]
cc_c = cc.encrypt(cc_p)
print('Key2:', cc_c)

# Result
print(ac.encrypt(FLAG))