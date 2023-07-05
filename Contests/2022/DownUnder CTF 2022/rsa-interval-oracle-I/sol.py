from sage.all import *
from pwn import *
from Crypto.Util.number import *

def add_intervals(lo: int, up: int) -> None:
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b'Lower bound: ', str(lo).encode())
    io.sendlineafter(b'Upper bound: ', str(up).encode())

def query(c: int) -> int:
    io.sendlineafter(b'> ', b'2')
    io.sendlineafter(b'queries: ', str(c).encode())
    return int(io.recvline())

io = process(["python", "chall.py"])
N = int(io.recvline())
c = int(io.recvline())

lo, up = 0, N
while lo <= up:
    mid = (lo + up)//2 
    add_intervals(lo, mid)
    if query(c) == 0:
        up = mid - 1
    else:
        lo = mid + 1 

io.sendlineafter(b'> ', b'3')
for m in range(lo - 10, lo + 10):
    if pow(m, 0x10001, N) == c:
        io.sendlineafter(b'Enter secret: ', str(m).encode())
        print(io.recvline())
        exit()

