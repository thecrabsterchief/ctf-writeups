from sage.all import *
from pwn import *
import json
from aes import decrypt_flag

from CryptoTools.own.smooth_primes import get_smooth_prime

io = remote("socket.cryptohack.org", 13378)

io.recvuntil(b"Alice: ")
alice = json.loads(io.recvline().strip().decode())
p = int(alice['p'], 16)
A = int(alice['A'], 16)

io.recvuntil(b"Bob: ")
bob = json.loads(io.recvline().strip().decode())


io.recvuntil(b"Alice: ")
enc_alice = json.loads(io.recvline().strip().decode())

q = get_smooth_prime(2048)[0]
g = int(alice["g"], 16)
 
alice["p"] = hex(q)
io.sendlineafter(b": ", json.dumps(alice).encode())

io.recvuntil(b"you: ")
B = int(json.loads(io.recvline().strip().decode())["B"], 16)
io.close()

Fq = GF(q)
b = ZZ(discrete_log(Fq(B), Fq(g), operation='*'))

shared_secret = pow(A, b, p)
flag = decrypt_flag(shared_secret, enc_alice['iv'], enc_alice['encrypted'])
print("Flag: " + flag)

# Flag: crypto{uns4f3_pr1m3_sm4ll_oRd3r}