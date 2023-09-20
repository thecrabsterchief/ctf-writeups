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
    indexs  = sum(spiralRight(indexs), [])

    ciphertexts = [
        encrypt(bytearray([i] + [0]*15)) 
            for i in tqdm(range(255), desc="Getting ciphertexts...")
    ]

    KEY = [[] for i in range(16)]
    pbar = tqdm(range(16))
    for i in pbar:
        pbar.set_description(f"Brute KEY[{i}]...")

        for k in range(255):
            ok = 0
            for enc in ciphertexts:
                c = (enc[i] - k) % 255
                c = SBOX.index(c)
                ok = (ok + c) % 255

            if ok == 0:
                KEY[i].append(k)
    
    for key in product(*KEY):
        cipher = Spiral(key=bytes(key))
        try:
            flag = unpad(cipher.decrypt(ct), 16)
            assert flag.startswith(b"maple{")

            print(flag)
        except:
            pass
            