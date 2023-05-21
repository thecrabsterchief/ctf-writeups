from Crypto.Util.number import getPrime, bytes_to_long
from secret import flag

e = 257
P = bytes_to_long(flag)

while True:
    p = getPrime(1024)
    if (p - 1) % e**2 != 0 and (p - 1) % e == 0:
        break

q = getPrime(1024)

n = p * q

C = pow(P, e, n)

assert (q - 1) % e != 0
assert (p - 1) % e == 0
assert (p - 1) % e**2 != 0

print(f"p = {p}")
print(f"q = {q}")
print(f"e = {e}")
print(f"n = {n}")
print(f"C = {C}")
