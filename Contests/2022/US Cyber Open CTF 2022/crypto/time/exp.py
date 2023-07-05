from pwn import *
import time
from string import *

context.log_level = 'error'


def guess(flag):
    p = process(["python", "chall.py"])

    st = time.time()
    p.sendlineafter(b">>> ", flag.encode())
    p.recvuntil(b"[")
    en = time.time()

    p.close()
    return round((en - st)*1000)

letter = ascii_lowercase + digits + "{}_"
flag = ""
while not flag.endswith("}"):
    candidate = []
    for char in letter:
        candidate.append(guess(flag + char))
    flag += letter[candidate.index(max(candidate))]
    print(flag)

