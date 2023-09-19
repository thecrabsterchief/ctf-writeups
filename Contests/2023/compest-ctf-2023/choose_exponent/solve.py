from pwn import *
from Crypto.Util.number import *

def get(e: int):
    io.sendlineafter(b">> ", b"1")
    io.sendlineafter(b": ", str(e).encode())
    io.recvuntil(b"flag: ")
    return int(io.recvline())


if __name__ == "__main__":
    io = process(["python3", "chall.py"])

    c1 = get(-1)
    c3 = get(-3)
    c5 = get(-5)
    N  = GCD(c1**3 - c3, c1**5 - c5)
    m  = pow(c1, -1, N)
    print(long_to_bytes(m).strip(b'\x00'))