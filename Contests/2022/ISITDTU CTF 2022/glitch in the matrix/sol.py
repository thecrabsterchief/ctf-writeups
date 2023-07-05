from sage.all import *
from pwn import *

def get_ciphertext():
    io.sendlineafter(b'Your option> ', b'2')
    io.recvuntil(b'Leaky ciphertext: ')

    ct =  bytes.fromhex(io.recvline()[:-1].decode())
    ct_bin = [int(x) for x in "".join(bin(b)[2:].zfill(8) for b in ct)]
    return [ct_bin[i:i + 128] for i in range(0, len(ct_bin), 128)]

def get_flag(pwd):
    io.sendlineafter(b'Your option> ', b'1')
    io.sendlineafter(b'Input your password (hex): ', pwd.encode())

    print(io.recvline())

if __name__ == '__main__':
    # io = process(["python", "chall.py"])
    io = remote("34.132.73.130", 8002)
    
    ct_blocks = [[] for _ in range(64)]
    for _ in range(128):
        for i, block in enumerate(get_ciphertext()):
            ct_blocks[i] += block
    
    MTR_s = []
    for block in ct_blocks:
        MTR_s.append(matrix(GF(2), 128, 128, block))

    pwd = "0"   # suppose that first bit = "0"
    for i in range(1, 64):
        check = MTR_s[i] + MTR_s[0]
        if check.rank() == 64: pwd += "0"
        else: pwd += "1"

    pwd = bytes([int(pwd[i:i+8], 2) for i in range(0, len(pwd), 8)]).hex()

    get_flag(pwd)

# Flag: ISITDTU{c8ac07f0e7d322179d5e6cfe78e5f70fc4ddc78d}