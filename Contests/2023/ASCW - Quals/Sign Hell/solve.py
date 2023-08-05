from pwn import *
from Crypto.Util.number import *

def _solve(a, b, n):
    # ax = b [mod n]
    d = GCD(a, GCD(b, n))
    return (b//d) * pow(a//d, -1, n//d) % (n//d)
def solve():
    io = remote("34.154.18.2", 6951)

    io.recvuntil(b"Public:  ", timeout=60)
    p, g, A = eval(io.recvline().strip().decode())

    s1, r1, m1 = [int(x) for x in io.recvline().split()]
    s2, r2, m2 = [int(x) for x in io.recvline().split()]

    # r1/r2 = (m1 - a*s1)/(m2 - a*s2) [p - 1]
    # r1*(m2 - a*s2) = r2*(m1 - a*s1) [p - 1]
    # r1*m2 - r2*m1 = a(r1*s2 - r2*s1)

    return long_to_bytes(_solve((r1*s2 - r2*s1), r1*m2 - r2*m1, p - 1))
 
if __name__ == "__main__":
    flag = solve()
    print(flag)