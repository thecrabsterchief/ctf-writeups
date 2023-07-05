from Crypto.Util.number import *
import hashlib
from pwn import *

def get_pubkey():
    n = int(io.recvline()[4:].decode())
    g = int(io.recvline()[4:].decode())

    return (n, g)

def get_enc_secret():
    return int(io.recvline()[4:].decode())

def send(cs):
    for c in cs:
        io.sendline(str(c).encode())
    
    B = []
    for _ in range(20):
        rec = io.recvline()
        if rec == b'\xf0\x9f\x98\xa1\n':
            B.append([_, False])
        else:
            B.append([_, True])
    return B

def genspace(SPACE, i, ok):
    if ok:
        return [sp for sp in SPACE if b'0' in sp[i : i + 7]]
    return [sp for sp in SPACE if b'0' not in sp[i : i + 7]]

def gencip(c0, i):
    u = bytes_to_long(b'\x01'  + b'\x00' * 128 )
    v = bytes_to_long(b'\x00' * i + b'0' * 7  + b'\x00' * (128 - 7 - i))
    m = (u - v) % n
    return (c0 * pow(g, m, n**2)) % n**2


if __name__ == '__main__':
    io = remote("maybe-someday.2022.ctfcompetition.com", 1337)
    io.recvuntil(b'== proof-of-work: disabled ==\n')
    n, g = get_pubkey()
    
    space = []
    for i in range(256):
        for j in range(256):
            m = hashlib.sha512(bytes([i]) + bytes([j])).hexdigest().encode()
            space.append(m)

    for _ in range(16):
        print(f'[+] Test {_}...')
        c0 = get_enc_secret()

        cs = [gencip(c0, i) for i in range(0, 121, 7)] + [0, 0]
        assert len(cs) == 20
        check  = send(cs)
        

        for (i, ok) in check:
            space = genspace(space, 7*i, ok)
        

        io.sendline(space[0])
        print(io.recvline())

    print(io.recvline())
