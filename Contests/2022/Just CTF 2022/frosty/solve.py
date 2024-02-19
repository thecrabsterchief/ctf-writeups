from pwn import *
import json
import hashlib
from fastecdsa.curve import P192 as Curve
from fastecdsa.point import Point

G = Curve.G
N = Curve.q.bit_length()

def coords(p : Point):
  return (hex(p.x)[2:], hex(p.y)[2:])

def mod_hash(msg : bytes, R : Point) -> int:
  h = hashlib.sha256()
  h.update(len(msg).to_bytes(64, 'big'))
  h.update(msg)
  h.update(R.x.to_bytes(N//8, 'big'))
  h.update(R.y.to_bytes(N//8, 'big'))
  return int(h.hexdigest(), 16) % Curve.q

def send(io, data):
  io.sendline(json.dumps(data).encode())

if __name__ == "__main__":
  io = process(["python3", "frosty.py"])
  io.recvline()

  h = mod_hash(b"Gimme!", G - G)
  send(io, {
    "op": "verify",
    "m": b"Gimme!".hex(),
    "z": hex(h),
    "c": hex(h),
    "pubkey": coords(G),
  })

  io.interactive()
