#!/usr/bin/python3
from Crypto.Util.number import getPrime
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import hashlib
import random

class Person(object):
    def __init__(self, p):
        self.p = p
        self.g = 2
        self.x = random.randint(2, self.p - 1)
    
    def calc_key(self):
        self.k = pow(self.g, self.x, self.p)
        return self.k

    def set_shared_key(self, k):
        self.sk = pow(k, self.x, self.p)
        aes_key = hashlib.md5(str(self.sk).encode()).digest()
        self.cipher = AES.new(aes_key, AES.MODE_ECB)

    def encrypt(self, pt):
        return self.cipher.encrypt(pad(pt, 16)).hex()

    def decrypt(self, ct):
        return unpad(self.cipher.decrypt(bytes.fromhex(ct)), 16)

flag = open("flag", "r").read().encode()
prime = getPrime(1024)
print(f"Prime: {hex(prime)}")
alice = Person(prime)
bob = Person(prime)

alice_k = alice.calc_key()
print(f"Alice sends her key to Bob. Key: {hex(alice_k)}")
print("Let's inturrupt !")
alice_k = int(input(">> "))
if alice_k == alice.g:
    exit("Malicious key !!")
bob.set_shared_key(alice_k)

bob_k = bob.calc_key()
print(f"Bob sends his key to Alice. Key: {hex(bob_k)}")
print("Let's inturrupt !")
bob_k = int(input(">> "))
if bob_k == bob.g:
    exit("Malicious key !!")
alice.set_shared_key(bob_k)

print("They are sharing the part of flag")
print(f"Alice: {alice.encrypt(flag[:len(flag) // 2])}")
print(f"Bob: {bob.encrypt(flag[len(flag) // 2:])}")
