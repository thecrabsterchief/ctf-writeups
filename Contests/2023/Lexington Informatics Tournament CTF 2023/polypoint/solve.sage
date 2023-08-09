from Crypto.Util.number import *


mat = []

with open("./encoded.txt", "r") as f:
    for _ in range(10):
        x, y = eval(f.readline().strip())
        
        row  = [x**i for i in reversed(range(11))] + [y]
        mat.append(row)

mat  = matrix(ZZ, mat)
last = mat.rref()[-1]
p, q = last[-2:]

# a1 + p*a0 == q

m, n = p.as_integer_ratio()
u, v = q.as_integer_ratio()
A, B, C = n*v, m*v, n*u

# A*a1 + B*a0 == C

_, x0, y0 = xgcd(A, B)
x0 *= C//_ 
y0 *= C//_ 

tx = B//gcd(A, B)
ty = A//gcd(A, B)

tx_ = (x0 - 10**12)//tx

for k in range(tx_, tx_  + 5):
    a1 = x0 - k*tx 
    if a1 > 10**11 and a1 < 10**12:
        a0 = (C - A*a1)//B 
        print(long_to_bytes(ZZ(a0)))