from pwn import *
from os import urandom

def xor(a, b):
    return bytes([x^y for x,y in zip(a, b)])

io = process(["python", "ofb.py"])
plaintext = b'Decrypt this... '  

iv = urandom(16)
io.sendlineafter(b"iv: ", iv.hex().encode())
c1 = bytes.fromhex(io.recvline()[:-1].decode())

io.sendlineafter(b"iv: ", xor(c1[:16], plaintext).hex().encode())
c2 = bytes.fromhex(io.recvline()[:-1].decode())

ct = xor(c2[:-16], c1[16:])
blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]

for block in blocks:
    plaintext += xor(block, plaintext[-16:])

print(plaintext)
# DUCTF{0fb_mu5t_4ctu4lly_st4nd_f0r_0bvi0usly_f4ul7y_bl0ck_c1ph3r_m0d3_0f_0p3ra710n_7b9cb403e8332c980456b17a00abd51049cb8207581c274fcb233f3a43df4a}
