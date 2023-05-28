from sage.all import *
from pwn import *
import json
from aes import decrypt_flag

io = remote("socket.cryptohack.org", 13373)

io.recvuntil(b"Alice: ")
alice = json.loads(io.recvline().strip().decode())
A = alice['A']

io.recvuntil(b"Bob: ")
bob = json.loads(io.recvline().strip().decode())


io.recvuntil(b"Alice: ")
enc_alice = json.loads(io.recvline().strip().decode())

alice['g'] = alice["A"]
alice['A'] = "0x00"
io.sendlineafter(b": ", json.dumps(alice).encode())

io.recvuntil(b"you: ")
shared_secret = int(json.loads(io.recvline().strip().decode())["B"], 16)

io.recvuntil(b"you: ")
enc_bob = json.loads(io.recvline().strip().decode())
io.close()

flag = decrypt_flag(shared_secret, enc_alice['iv'], enc_alice['encrypted'])
print("Flag: " + flag)
# Flag: crypto{n07_3ph3m3r4l_3n0u6h}