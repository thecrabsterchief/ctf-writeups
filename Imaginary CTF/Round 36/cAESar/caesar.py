#!/usr/bin/env python3

from Crypto.Cipher import AES
from random import randint

flag = b"ictf{REDACTED}"

key = b"_verysecurekey_!"
cipher = AES.new(key, AES.MODE_ECB)

out = []
s = randint(0, 2**64)
ct = cipher.encrypt(flag.ljust(64, b'\0'))
for n in ct:
  out.append((n + s) % 256)

print(bytes(out))

# b'\xe4\xda\xdbD\x82(\x0c\x9bR\xcc\t\xcb\xe6\x14\xbc\x1e\x87\xf5\x06\xc0-K\xe2A\xdc}\x03\xc7^e\xa0i\xed\xbc[*\x91yG\x90\xa6\xe6\xed\xbf4EY\xe3A\\\x8c\x86=V#u0\x8b\xe3\xb1\x91Q)D'
