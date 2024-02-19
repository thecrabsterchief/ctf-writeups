from pwn import *
import json
import hashlib
from fastecdsa.curve import P192 as Curve
from fastecdsa.point import Point

G = Curve.G
N = Curve.q.bit_length()
client_prikey = 0xee669fa9dc3e12154d13ac6bc17d6c3b2291832dadd76746
client_pubkey = client_prikey * G
server_pubkey = Point(0x9532cae35947c6211c2f808145aa193f9773e591b03f3e1b, 0x3df6739646175efd21fe509d8b1f436fa4f6663b4eec9641, Curve)
pubkey = client_pubkey + server_pubkey

def parse_ec(p):
  return Point(int(p[0], 16), int(p[1], 16), Curve)

def coords(p : Point):
  return (hex(p.x)[2:], hex(p.y)[2:])

def mod_hash(msg : bytes, R : Point) -> int:
  h = hashlib.sha256()
  h.update(len(msg).to_bytes(64, 'big'))
  h.update(msg)
  h.update(R.x.to_bytes(N//8, 'big'))
  h.update(R.y.to_bytes(N//8, 'big'))
  return int(h.hexdigest(), 16) % Curve.q

def send_json(io, data):
  io.sendline(json.dumps(data).encode())

def load_json(io):
  return json.loads(io.recvline().strip().decode())

def sign(io, msg=b"vnc"):
  send_json(io, {"op": "sign"})
  public_nonce = load_json(io)["D"]
  send_json(io, {"D": public_nonce, "msg": msg.hex()})
  z = int(load_json(io)["z"], 16)
  c = mod_hash(b"vnc", 2*parse_ec(public_nonce))
  return z//c

def connect():
  return process(["python3", "frosty.py"])

if __name__ == "__main__":
  brute = []

  for _ in range(10):
    io = connect()
    io.recvline()
    brute.append(sign(io))
    io.close()
  
  server_prikey = min(brute)
  
  io = connect()
  c = mod_hash(b"Gimme!", G-G)
  send_json(io, {
    "op": "verify",
    "m": b"Gimme!".hex(),
    "c": hex(c)[2:],
    "z": hex(c * (client_prikey + server_prikey))[2:], 
  })

  io.interactive()