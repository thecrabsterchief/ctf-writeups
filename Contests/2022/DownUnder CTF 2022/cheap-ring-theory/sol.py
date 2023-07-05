from pwn import *

p = process(["python", "crt.py"])
for i in range(3): p.recvline()
for i in range(3): p.sendline(b"0 0 0")
p.interactive()
