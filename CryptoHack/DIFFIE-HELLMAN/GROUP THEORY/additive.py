from pwn import *
import json
from aes import decrypt_flag

io = remote("socket.cryptohack.org", 13380)

io.recvuntil(b"Alice: ")
alice = json.loads(io.recvline().strip().decode())
p = int(alice['p'], 16)
g = int(alice['g'], 16)
A = int(alice['A'], 16)

io.recvuntil(b"Bob: ")
bob = json.loads(io.recvline().strip().decode())
B = int(bob['B'], 16)

io.recvuntil(b"Alice: ")
enc = json.loads(io.recvline().strip().decode())
io.close()

iv = enc['iv']
ct = enc['encrypted']
shared_secret = A * B * pow(g, -1, p) % p
flag = decrypt_flag(shared_secret, iv, ct)

print("Flag: " + flag)
# Flag: crypto{cycl1c_6r0up_und3r_4dd1710n?}