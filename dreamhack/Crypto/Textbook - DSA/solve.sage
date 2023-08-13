from pwn import *
from Crypto.Util.number import *
from hashlib import sha1
    
io = remote("host3.dreamhack.games", int(22066))

def sign(msg: bytes):
    io.sendline(b"1")
    io.sendlineafter(b": ", msg.hex().encode())
    r, s = eval(io.recvline().decode().strip())
    return bytes_to_long(sha1(msg).digest()), (r, s)


def verify(msg, r, s):
    io.sendline(b"2")
    io.sendlineafter(b": ", msg.hex().encode())
    io.sendlineafter(b": ", b", ".join([str(x).encode() for x in [r, s]]))
    print(io.recvline())
    print(io.recvline())

def get_info():
    io.sendline(b"3")
    io.recvuntil(b"p = "); p = int(io.recvline())
    io.recvuntil(b"q = "); q = int(io.recvline())
    io.recvuntil(b"g = "); g = int(io.recvline())
    io.recvuntil(b"token = "); token = eval(io.recvline().decode().strip())

    return p, q, g, token

def _sign(msg, g, p, q, k, x):
        r = pow(g, k, p) % q
        h = bytes_to_long(sha1(msg).digest())
        s = inverse(k, q) * (h + x * r) % q
        return (r, s)

if __name__ == "__main__":
    p, q, g, token = get_info()
    h, (r, s)      = sign(b"hacker")

    F = GF(q)
    Px.<x> = PolynomialRing(F)
    fx = x * (h + x*r) - s

    for _x, _ in fx.roots():
        k = F(1)/F(_x)
        r, s = _sign(token, g, p, q, int(k), int(_x))
        verify(token, r, s)