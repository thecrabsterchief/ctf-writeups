#!/usr/bin/env python3

from sneaky import n
from Crypto.Util.number import bytes_to_long

m = bytes_to_long(open("flag.txt", "rb").read())
e = 65537
c = pow(m, e, n)

print(f"{n = }")
print(f"{e = }")
print(f"{c = }")
