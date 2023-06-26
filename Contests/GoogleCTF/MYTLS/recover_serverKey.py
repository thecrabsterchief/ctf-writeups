from pwn import *
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
from tqdm import tqdm

def print_encrypted(message, iv, key):
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(binascii.unhexlify(iv)))
    encryptor = cipher.encryptor()
    message = message.encode('utf-8')
    payload = encryptor.update(
        message + b'\x00' * (16 - len(message) % 16)) + encryptor.finalize()
    return binascii.hexlify(payload).decode('utf-8')


def input_encrypted(iv, key):
  cipher = Cipher(
      algorithms.AES(key),
      modes.CBC(binascii.unhexlify(iv)))
  decryptor = cipher.decryptor()
  payload = input()
  payload = binascii.unhexlify(payload)
  res = decryptor.update(payload)
  return res.strip(b'\x00')

def print_decrypted(message, iv, key):
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(binascii.unhexlify(iv)))
    encryptor = cipher.decryptor()
    message = bytes.fromhex(message)
    return encryptor.update(message).decode().strip("\x00").split("Saved! Previous secret reference: ")[-1]

# io = process("python3 server.py".split())
io = remote("mytls.2023.ctfcompetition.com", 1337)
io.recvline()

# Getting the client private key.
with open('./src/guest-ecdhkey.pem', 'rb') as client_key_file:
    client_key = serialization.load_pem_private_key(client_key_file.read(),
                                                    None, default_backend())

# Getting the CA cert.
with open('./src/ca-crt.pem', 'rb') as ca_file:
    ca = x509.load_pem_x509_certificate(ca_file.read())

# Getting the client cert.
with open('./src/guest-ecdhcert.pem', 'rb') as client_cert_file:
    client_cert_content = client_cert_file.read()
    client_cert = x509.load_pem_x509_certificate(client_cert_content)

# Receive the server cert.
server_cert = x509.load_pem_x509_certificate(
    io.recvuntil(b"-----END CERTIFICATE-----\n")
)

# Checking the server key, this is important. We don't want fakes here!
ca.public_key().verify(
    server_cert.signature,
    server_cert.tbs_certificate_bytes,
    padding.PKCS1v15(),
    server_cert.signature_hash_algorithm
)

# Send client cert to server
io.sendlineafter(b":\n", client_cert_content)

# Generate ephemeral server random
client_ephemeral_random = token_hex(16)

# Generate ephemeral client key
client_ephemeral_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
client_ephemeral_public_key = client_ephemeral_key.public_key()

# Send the ephemeral client random to server
io.sendlineafter(b":\n", client_ephemeral_random.encode())

# Send the ephemeral client key to server
io.sendlineafter(b":\n", client_ephemeral_public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo)
)

# Receive the server ephemeral  random
io.recvuntil(b"Server ephemeral random:\n")
server_ephemeral_random = io.recv(32).decode()

# Receive the Server ephemeral key
io.recvuntil(b"Server ephemeral key:\n")
server_ephemeral_public_key = serialization.load_pem_public_key(
    io.recvuntil(b"-----END PUBLIC KEY-----\n")
)

# Generate ephemeral client key
client_ephemeral_secret = client_ephemeral_key.exchange(
    ec.ECDH(), server_ephemeral_public_key
)
client_secret = client_key.exchange(ec.ECDH(), server_cert.public_key())
derived_key = HKDF(algorithm=hashes.SHA256(),
    length=32,
    salt=b'SaltyMcSaltFace',
    info=b'mytls'
).derive(
    client_ephemeral_secret +
    client_secret +
    client_ephemeral_random.encode('utf-8') +
    server_ephemeral_random.encode('utf-8') 
)

# Generate client hmac
client_hmac = hmac.HMAC(derived_key, hashes.SHA256())
client_hmac.update(b'client myTLS successful!')
io.sendlineafter(b":\n", binascii.hexlify(client_hmac.finalize()))

# Final verify step
io.recvuntil(b"Server HMAC:\n")
server_hmac_content = io.recvline()[:-1].decode()
server_hmac = hmac.HMAC(derived_key, hashes.SHA256())
server_hmac.update(b'server myTLS successful!')
server_hmac.verify(binascii.unhexlify(server_hmac_content))

# Exploit here

print_decrypted(io.recvline()[:-1].decode(), server_ephemeral_random, derived_key)
with open("log.txt", "w+") as f:
    for i in tqdm(range(241)):
        io.recvline()
        io.sendline(print_encrypted("../../app/server-ecdhkey.pem", server_ephemeral_random, derived_key).encode())
        io.recvline()
        io.sendline(print_encrypted("1"*(i + 1), server_ephemeral_random, derived_key).encode())
        leak = print_decrypted(io.recvline()[:-1].decode(), server_ephemeral_random, derived_key)
        f.write(leak + "\n")

io.close()

# recover server private key
from hashlib import sha256
from string import printable as table

key_len = 241
leak = open("./log.txt", "r").read().split("\n")
recovered = ""

for i in reversed(range(key_len)):
    for char in table:
        suffix = char.encode() + recovered.encode()
        if sha256(b"1"*i + suffix).hexdigest() == leak[i]:
            recovered = char + recovered
            break

print(recovered)
with open("./server-ecdhkey.pem", "w") as f:
    f.write(recovered)