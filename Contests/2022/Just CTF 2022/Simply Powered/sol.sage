from minipwn import *

io = remote("simply-powered-ams3.nc.jctf.pro", 4444)

for _ in range(100):
   io.recvuntil(b'e = ')
   e = int(io.recvline())

   io.recvuntil(b'p = ')
   p = int(io.recvline())

   io.recvline()
   cmd = io.recvline()[:-1].decode()

   exec(f"MT = {cmd[:7]} GF({p}), {cmd[7:]}")
   d = inverse_mod(e, MT.multiplicative_order())
   M = MT^d

   M = M.change_ring(ZZ)
   s = sum(sum(M))

   io.recvuntil(b'We expect you to provide sum(M % p) - sum of all elements in M % p.\n')
   io.sendline(str(s).encode())
   print(io.recvline())
