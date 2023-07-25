from pwn import *
from Crypto.Util.number import *

io = process(["python3", "rsa2.py"])

# n, e, c
io.recvuntil(b"n = "); n = int(io.recvline())
io.recvuntil(b"e = "); e = int(io.recvline())
io.recvuntil(b"c = "); c = int(io.recvline())

io.sendlineafter(b": ", str(c * pow(2, e, n) % n).encode())
io.recvuntil(b"m = "); m2 = int(io.recvline())

flag = long_to_bytes(m2 * pow(2, -1, n) % n)
print("Flag:", flag.decode())