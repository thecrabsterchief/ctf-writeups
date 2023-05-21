from Crypto.Util.number import *
from sympy import nextprime

flag = b'DH{?????????????????????????????????????????}'

q = getPrime(1024)
p = nextprime(q + 1)
N = p * q
while True:
    e = getPrime(256)
    if GCD(e, (p - 1) * (q - 1)) == 1:
        d = inverse(e, (p - 1) * (q - 1))
        break
dp = d % (p - 1)
dq = d % (q - 1)
qinv = inverse(q, p)

print(f'N = {N}')
print(f'dp = {dp}')
print(f'dq = {dq}')
print(f'qinv = {qinv}')
print(f'encrypted flag = {pow(bytes_to_long(flag), e, N)}')