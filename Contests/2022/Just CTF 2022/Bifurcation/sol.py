from pwn import *

io = remote('bifurcation.nc.jctf.pro', 31789)

io.sendlineafter(b'Your move!> ', b'dss')
io.sendlineafter(b'Your move!> ', b'dwww')
io.sendlineafter(b'Your move!> ', b'ssa')
io.sendlineafter(b'Your move!> ', b'dww')
io.sendlineafter(b'Your move!> ', b'ssssssaaa')
io.sendlineafter(b'Your move!> ', b'ddddddddddddddww')
io.sendlineafter(b'Your move!> ', b'ssssssssssssssssssssssssssaaaaa')
io.sendlineafter(b'Your move!> ', b'dddddw')
io.sendlineafter(b'Your move!> ', b'awww')
io.sendlineafter(b'Your move!> ', b'aass')
io.sendlineafter(b'Your move!> ', b'asss')
io.sendlineafter(b'Your move!> ', b'dddds')
io.sendlineafter(b'Your move!> ', b'ddwwww')
io.sendlineafter(b'Your move!> ', b'saaaaaa')
io.sendlineafter(b'Your move!> ', b'saad')
io.sendlineafter(b'Your move!> ', b'ssaa')
io.sendlineafter(b'Your move!> ', b'dw')
io.sendlineafter(b'Your move!> ', b'ddw')
io.sendlineafter(b'Your move!> ', b'dddddds')
io.sendlineafter(b'Your move!> ', b'dddwww')
io.sendlineafter(b'Your move!> ', b'saaaaaa')
io.sendlineafter(b'Your move!> ', b'dw')
io.sendlineafter(b'Your move!> ', b'aawww')

io.recvuntil(b'Current flag: ')
flag = io.recvline()[:-1].decode()

print(f"[+] Flag: {flag}")
# Flag: justCTF{uCA8ysuM8q9BTp}