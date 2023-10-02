from pwn import *
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
from Crypto.Util.number import *
from tqdm import tqdm

def bxor(a, b):
  return bytes([i ^ j for i, j in zip(a, b)])


def expand_key(key, n):
  if len(key) >= n:
    return key[:n]

  out = key + b"\x00" * (n - len(key))
  for i in range(1, n - len(key) + 1):
    out = bxor(out, b"\x00" * i + key + b"\x00" * (n - len(key) - i))
  return out

def generate_challenge_response(challenge_hash, keys):
  k1, k2, k3 = keys
  challenge_response = DES.new(
      expand_key(k1, 8), DES.MODE_ECB
  ).encrypt(pad(challenge_hash, 16))
  challenge_response += DES.new(
      expand_key(k2, 8), DES.MODE_ECB
  ).encrypt(pad(challenge_hash, 16))
  challenge_response += DES.new(
      expand_key(k3, 8), DES.MODE_ECB
  ).encrypt(pad(challenge_hash, 16))

  return challenge_response

def brute_key(challenge_response, challenge_hash):
  blocks = [challenge_response[i:i+16] for i in range(0, 3*16, 16)]
  res = [0, 0, 0]
  for k in tqdm(range(255*(256**2 + 256 + 1) + 1)):
    key = k.to_bytes(length=3, byteorder='big')
    ok = DES.new(
      expand_key(key, 8), DES.MODE_ECB
    ).encrypt(pad(challenge_hash, 16))
    if ok in blocks:
      print("Found!", key, blocks.index(ok))
      res[blocks.index(ok)] = key
      if all([x != 0 for x in res]):
        return res

# a b c 0 0 0 0 0
# 0 a b c 0 0 0 0
# 0 0 a b c 0 0 0
# 0 0 0 a b c 0 0
# 0 0 0 0 a b c 0
# 0 0 0 0 0 a b c

if __name__ == "__main__":
  # io = process(["python3", "server.py"])
  io = remote("handshake.ctf.maplebacon.org", 1337)

  io.recvline()
  traffic = eval(io.recvline().strip().decode())
  chal_res, chal_hash, _ = traffic[2][1]

  io.recvuntil(b"Server challenge: ")
  ser_chal = eval(io.recvline().strip().decode())

  keys = brute_key(chal_res, chal_hash)
  res = generate_challenge_response(b'hack', keys)

  io.sendline(f"{res.hex()} {b'hack'.hex()} admin")

  io.interactive()