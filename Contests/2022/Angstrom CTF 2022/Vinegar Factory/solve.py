#
# Author: vnc1106
# Created: 2024-02-10 08:54:44
#

from pwn import *
import string

alpha = string.ascii_lowercase
def decrypt(ct, key):
  ret = ""
  i = 0
  for c in ct:
    if c in alpha:
      ret += alpha[(alpha.index(c) - alpha.index(key[i])) % len(alpha)]
      i = (i + 1) % len(key)
    else:
      ret += c
  return ret

def solve(i):
  info(f"Solving Round {i}")
  io.recvuntil(f"Challenge {i}: ".encode())
  chall = io.recvline().decode().strip()
  
  for start in range(len(chall)):
    encrypted = chall[start:]
    key = decrypt(encrypted[:4], "actf")
    try:
      fleg = decrypt(encrypted, key).split("fleg")[0]
      if fleg.startswith("actf{") and fleg.endswith("}") \
        and fleg.count("{") == 1 and fleg.count("}") == 1:
        
        info(f"Flag Round {i}: {fleg}")
        io.sendlineafter(b"> ", fleg.encode())
        break
    except:
      pass

if __name__ == "__main__":
  io = process(["python3", "main.py"])
  # io = remote("challs.actf.co", 31333)

  for i in range(50):
    solve(i)
  io.close()