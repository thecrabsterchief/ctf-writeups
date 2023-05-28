from sage.all import *
from pwn import *
import json
from aes import decrypt_flag

io = remote("socket.cryptohack.org", 13379)

io.sendlineafter(b"Bob: ", json.dumps({"supported": ["DH64"]}).encode())
io.sendlineafter(b"Alice: ", json.dumps({"chosen": "DH64"}).encode())

io.recvuntil(b"Alice: ")
alice = json.loads(io.recvline().strip().decode())

io.recvuntil(b"Bob: ")
bob = json.loads(io.recvline().strip().decode())

io.recvuntil(b"Alice: ")
enc = json.loads(io.recvline().strip().decode())
io.close()

p = int(alice['p'], 16)
g = int(alice['g'], 16)
A = int(alice['A'], 16)
B = int(bob['B'], 16)
iv = enc['iv']
ct = enc['encrypted_flag']

F = GF(p)
a = discrete_log(F(A), F(g), operation="*")
shared_secret = pow(B, ZZ(a), p)

flag = decrypt_flag(shared_secret, iv, ct)
print("Flag: " + flag)
# Flag: crypto{d0wn6r4d35_4r3_d4n63r0u5}