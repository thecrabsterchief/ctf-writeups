from pwn import *
from Crypto.Util.number import *

io = remote("be.ax", 31100)

io.recvuntil(b"n = "); n = int(io.recvline())
io.recvuntil(b"e = "); e = int(io.recvline())
io.recvuntil(b"ct = "); c = int(io.recvline())

io.sendlineafter(b"> ", str(pow(2, e, n) * c % n).encode())
flag = int(io.recvline()) * pow(2, -1, n) % n
io.close()

print(long_to_bytes(flag))
# corctf{h4ng_0n_th15_1s_3v3n_34s13r_th4n_4n_LSB_0r4cl3...4nyw4y_1snt_f1zzbuzz_s0_fun}