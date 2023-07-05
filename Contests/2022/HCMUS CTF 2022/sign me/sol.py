import hashlib
from Crypto.Util.number import *
from random import randint
from os import  urandom
from base64 import b64decode, b64encode
from hashlib import sha256
from pwn import *

s = remote("103.245.250.31", 31850)

def get():
    s.recvuntil(b'Select an option: ')
    s.sendline(b'0')
    g = int(s.recvline().decode()[3:])
    p = int(s.recvline().decode()[3:])
    return (g, p)

def sign(msg):
    send = b64encode(msg)
    s.recvuntil(b'Select an option: ')
    s.sendline(b'1')
    s.sendline(send)
    s.recvuntil(b'Input message you want to sign: Signature (r, s):  ')
    rr, ss = [int(x) for x in s.recvline().decode()[1:-2].split(', ')]

    # Find x ...
    h = bytes_to_long(sha256(send).digest())
    x = (h - ss) * inverse(rr, p - 1) % (p - 1)
    return [rr, ss, x]


def get_flag():
    s.recvuntil(b'Select an option: ')
    s.sendline(b'3')
    s.recvuntil(b"Could you sign this for me:  ")
    enc = s.recvline()[:-1]
    h = bytes_to_long(sha256(enc).digest())
    R = g
    S = (h - x*g) % (p - 1)
    
    s.recvuntil(b'Input r:')
    s.sendline(b64encode(long_to_bytes(R)))
    
    s.recvuntil(b'Input s:')
    s.sendline(b64encode(long_to_bytes(S)))
    
    try:
        s.recvuntil(b' Congratulation, this is your flag:  ')
        return(f"Flag >> {s.recvline()}")
        exit()
    except:
        return("g may be even! Let's reconnect again")


g, p = get()
rr, ss, x = sign(b'\00')

print(get_flag())

# Flag: HCMUS-CTF{B4se64_15_1nt3r3stin9}