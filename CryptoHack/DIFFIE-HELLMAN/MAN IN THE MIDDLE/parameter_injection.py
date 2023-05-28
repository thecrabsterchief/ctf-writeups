from pwn import *
import json
from aes import decrypt_flag


io = remote("socket.cryptohack.org", 13371)

io.recvuntil(b"Alice: ")
alice = json.loads(io.recvline().strip())
io.sendlineafter(b"Bob: ", json.dumps(alice).encode())

io.recvuntil(b"Bob: ")
bob = json.loads(io.recvline().strip())
bob['B'] = '0x00'

# man in middle
io.sendlineafter(b"Alice: ", json.dumps(bob).encode())

# get enc_flag
io.recvuntil(b"Alice: ")
enc = json.loads(io.recvline().strip())
io.close()

iv = enc['iv']
ct = enc['encrypted_flag']
shared_secret = 0
flag = decrypt_flag(shared_secret, iv, ct)

print("Flag: " + flag)
# Flag: crypto{n1c3_0n3_m4ll0ry!!!!!!!!}