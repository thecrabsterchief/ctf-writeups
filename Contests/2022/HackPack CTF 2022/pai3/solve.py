from pwn import *
from itertools import combinations
from Crypto.Util.number import *

def decrypt_msg(msg):
  io.sendlineafter(b">>>", b"D")
  io.sendlineafter(b">", str(msg).encode())
  io.recvuntil(b"MSG: ")
  return int(io.recvline())

def encrypt_flag():
  io.sendlineafter(b">>>", b"E")
  io.sendlineafter(b">>>", b"F")
  io.recvuntil(b"FLAG: ")
  return int(io.recvline())

if __name__ == "__main__":
  # io = remote("cha.hackpack.club", 10997)
  io = process(["python3", "paiaiai.py"])

  X = []
  for _ in range(10): # until we have D(Y) = {kp/(kp + kq)*flag, kq/(kp + kq)*flag}
    X.append(encrypt_flag())
  for c1, c2 in combinations(X, 2):
    m = long_to_bytes(decrypt_msg(c1 * c2))
    if b"flag" in m:
      print(m)
      exit()