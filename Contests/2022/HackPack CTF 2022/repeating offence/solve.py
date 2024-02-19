from pwn import *

E = 0x10001

def solve_stage(stage):
  io.recvuntil(b"N: "); N = int(io.recvline())
  io.recvuntil(b"G: "); G = int(io.recvline())
  io.recvuntil(b"(Password): "); C = int(io.recvline())

  if stage == 1:
    C_ = pow(C, pow(2, E, N), N**2)
  else:
    C_ = pow(C, 2, N**2)

  io.sendlineafter(b">>> ", b"D")
  io.sendlineafter(b"(int): ", str(C_).encode())
  io.recvuntil(b"MSG -> "); m = int(io.recvline())

  s = m * pow(2, -1, N) % N
  io.sendlineafter(b">>> ", b"S")
  io.sendlineafter(b"(int): ", str(s).encode())

if __name__ == "__main__":
  io = process(["python3", "repeatingoffense.py"])

  for stage in [1, 2]:
    solve_stage(stage)
  io.interactive()