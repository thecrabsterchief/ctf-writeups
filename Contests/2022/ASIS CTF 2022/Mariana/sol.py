from sage.all import *
from pwn import *

def sol():
    io.recvuntil(b'| p = ')
    p = int(io.recvline())
    io.recvuntil(b'| g = ')
    g = int(io.recvline())

    x = crt([1, g], [p - 1, p]) - p*(p - 1)
    io.sendlineafter(b'| Send the solution x = \n', str(x).encode())
    print(io.recvline())

    
io = remote("65.21.255.31", 32066)
for i in range(40):
    sol()

# FLag: ASIS{fiX3d_pOIn7s_f0r_d!5Cret3_l0g4riThmS!}