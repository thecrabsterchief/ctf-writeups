from pwn import *

io = process(["python3", "impossible.py"])
io.sendlineafter(b": ", str(2**65).encode())
io.sendlineafter(b": ", str(2**64 - 1).encode())

io.interactive()