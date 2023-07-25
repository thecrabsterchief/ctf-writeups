from pwn import *
from string import printable

io = process(["python3", "LazyLagrange.py"])

def query1(X):
    assert len(X) <= 10
    io.sendlineafter(b": ", b"1")
    io.sendlineafter(b"> ", " ".join(str(x) for x in X).encode())

    return [int(io.recvline()) for _ in range(len(X))]

def query2(X):
    io.sendlineafter(b": ", b"2")
    io.sendlineafter(b"> ", " ".join(str(x) for x in X).encode())

    return [int(x) for x in io.recvline().split()]

max_a = max(ord(c) for c in printable) + 1
y = query1([max_a])[0]
P.<x> = PolynomialRing(ZZ)
fx = P(0)

for i in range(18):
    a = (y - fx(max_a))//max_a**i % max_a
    fx += a*x**i

A = fx.coefficients()
perm = query2(A)
flag = [A[perm.index(i)] for i in range(18)]
print("Flag:", bytes(flag).decode())