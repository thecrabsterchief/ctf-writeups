from Crypto.Util.number import  long_to_bytes, bytes_to_long
from hashlib import sha256
from pwn import *

p = 81561774084914804116542793383590610809004606518687125749737444881352531178029
g = 2
q = p - 1

def hash(values):
    h = sha256()
    for v in values:
        h.update(long_to_bytes(v))
    return bytes_to_long(h.digest())

def verify_vote(encrypted_vote, proof, X):
    R, S = encrypted_vote
    c_0, c_1, f_0, f_1 = proof

    values = [
        pow(g, f_0, p) * pow(R, -c_0, p) % p,
        pow(X, f_0, p) * pow(S, -c_0, p) % p,
        pow(g, f_1, p) * pow(R, -c_1, p) % p,
        pow(X, f_1, p) * pow(S, -c_1, p) * pow(g, c_1, p) % p,
    ]

    print(values)
    return c_0 + c_1 == hash(values)

# R, S = g^y, g^(m + xy)
# (c0, c1, f0, f1) -> c0 + c1 = C

# f0   - c0*y              -> -c0*y
# f0*x - c0*(m + xy)       -> -c0*(xy - 100)
# f1   - c1*y              -> -c1*y
# f1*x - c1*(m + xy) + c1  -> -c1*(xy - 101)

# [0, c, -c1*y, -c1*(xy - 101)]

# choose: 
# c0 = f0 = f1 = 0
# -c1*y = i <- brute
# -c1*(xy - 101) = 1

def help(arr):
  return ", ".join([str(x) for x in arr]).encode()

for i in range(1, 10**3):
  try:
    c1 = hash([1, 1, pow(g, i, p), g])
    y = i * pow(-c1, -1, q) % q
    x = (101 + pow(-c1, -1, q)) % q
    x = x * pow(y, -1, q) % q
    X = pow(g, x, p)
    R = pow(g, y, p)
    S = pow(g, -100 + x*y, p)
    encrypted_vote = (R, S)
    proof = (0, c1, 0, 0)
    assert verify_vote(encrypted_vote, proof, X)
    print("=== Found ===")
    print(x)
    print(encrypted_vote)
    print(proof)
    print("=== Found ===")
    print("Connect to get flag...")

    io = remote("zkp.ctf.maplebacon.org", 1337)
    io.sendlineafter(b": ", str(x).encode())
    io.sendlineafter(b": ", help(encrypted_vote))
    io.sendlineafter(b": ", help(proof))
    break
  except:
    pass

io.interactive()