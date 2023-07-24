from Crypto.Util.number import *
from base64 import *
from pwn import xor

with open("./flag.enc", "rb") as f:
    ct = f.read()

assert len(ct) == 8*6
# prefix flag: "CCT"

# recover key
_ba = b64encode(b"CCTF{")[:6]
_baph, key = '', ''
for b in _ba.decode('utf-8'):
    if b.islower():
        _baph += b.upper()
        key += '0'
    else:
        _baph += b.lower()
        key += '1'

_baph = _baph.encode('utf-8')
key = xor(_baph, ct[:len(_baph)])

# recover flag
baph = xor(key, ct).decode()
ba = ''
for b in baph:
    if b.isupper():
        ba += b.lower()
    else:
        ba += b.upper()

flag = b64decode(ba)
print("Flag:", flag.decode())