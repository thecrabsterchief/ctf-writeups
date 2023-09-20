from tqdm import tqdm
from spiral import *
from itertools import product
from pwn import *
from Crypto.Util.Padding import unpad

def encrypt(payload: bytes):
    io.sendlineafter(b">>> ", b"2")
    io.sendline(payload.hex().encode())
    return bytes.fromhex(io.recvline().decode().strip())

def get_flag_enc():
    io.sendlineafter(b">>> ", b"1")
    return bytes.fromhex(io.recvline().decode().strip())

if __name__ == "__main__":
    io = remote("localhost", 1337)
    ct = get_flag_enc()

    indexs  = bytes2matrix(bytes(list(range(16))))
    indexs  = sum(spiralLeft(indexs), [])

    equations = []
    pbar = tqdm(range(16))
    for i in pbar:
        pbar.set_description(f"Brute key[{i}]...")

        payload = bytearray(16)
        CONST = 255
        for j in range(256):
            payload[i] = j
            CONST ^= encrypt(bytes(payload))[indexs[i]]

        equations.append(CONST)

    KEY = [[] for i in range(16)]
    for i in range(8):
        # SBOX[key[i]]    + key[15 - i] = equations[i]
        # SBOX[key[15-i]] + key[i]      = equations[15-i]

        for ki in range(256):
            c1 = (equations[i] - SBOX[ki % 255]) % 255
            c2 = SBOX.index((equations[15 - i] - ki) % 255)
            if c1 == c2:
                KEY[i].append(ki)
                KEY[15-i].append(c1)

    for _key in product(*KEY):
        try:
            flag = unpad(Spiral(bytes(_key),rounds=1).decrypt(ct), 16)
            print(flag)
        except:
            pass