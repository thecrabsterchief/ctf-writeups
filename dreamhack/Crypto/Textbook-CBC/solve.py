from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

BLOCK_SIZE = 16
_decrypt = lambda ct, key: unpad(AES.new(key, AES.MODE_CBC, key).decrypt(ct), BLOCK_SIZE)

def encrypt(msg):
    io.sendline(b"1")
    io.sendlineafter(b": ", msg.hex().encode())
    return bytes.fromhex(io.recvline().strip().decode())

def decrypt(ct):
    io.sendline(b"2")
    io.sendlineafter(b": ", ct.hex().encode())
    return bytes.fromhex(io.recvline().strip().decode())

def get_flag():
    io.sendline(b"3")
    io.recvuntil(b"flag = ")
    io.close()
    return bytes.fromhex(io.recvline().strip().decode())

io = remote("host3.dreamhack.games", 14830)
# io = process(["python3", "challenge.py"])

block = encrypt(b"a"*16)[:16]
ENC0  = encrypt(b"a"*16 + block)[16:32]

key = decrypt(ENC0 + b"\x0f"*16 + ENC0)[:16]
ct  = get_flag()
flag = _decrypt(ct, key)
print(flag)