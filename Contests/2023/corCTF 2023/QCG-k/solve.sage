from Crypto.Util.number import bytes_to_long
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES
from hashlib import sha256
import sys

sys.setrecursionlimit(10**8)

ct = bytes.fromhex("5c9d830f422288b4a9a37dc6b1cf68bfb7ee1acadb428d9fee6b17a8b8cbc5e7d871314bf090e4faa083d68162414b72992a60119ceb9c67f928d224f44f14c5")
iv = bytes.fromhex("bf549fa30bef66988268f357e1014c8d")

q = 77897050769654696452572824710099972349639759246855689360228775736949644730457

H = []
R = []
S_INV = []

with open("./quotes.txt", "rb") as f:
    for m in f.readlines():
        H.append(
            bytes_to_long(sha256(m.strip()).digest())
        )
with open("./out.txt", "rb") as f:
    out = f.readlines()
    for i in range(len(H)):
        (r, s) = eval(out[i].strip().decode())
        R += [r]
        S_INV += [pow(s, -1, q)]

F = GF(q)
Px = PolynomialRing(F, "x"); x = Px.gen()

def kij(i, j):
	hi, hj = F(H[i]), F(H[j])
	s_invi, s_invj = F(S_INV[i]), F(S_INV[j])
	ri, rj = F(R[i]), F(R[j])
	return x*(ri*s_invi - rj*s_invj) + hi*s_invi - hj*s_invj

def dpoly(n, i, j):
	if i == 0:
		return (kij(j+1, j+2))*(kij(j+1, j+2)) - (kij(j+2, j+3))*(kij(j+0, j+1))
	else:
		left = dpoly(n, i-1, j)
		for m in range(1,i+2):
			left  *= kij(j+m, j+i+2)
		right = dpoly(n, i-1, j+1)
		for m in range(1,i+2):
			right *= kij(j, j+m)
		return (left - right)

N = len(H)
pol = dpoly(N - 4, N - 4, 0)
for _x, _ in pol.roots():
    key = sha256(str(_x).encode()).digest()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    flag = cipher.decrypt(ct)
    if b'corctf' in flag:
	    print("[+] Flag:", unpad(flag, 16).decode())
	    
# corctf{wh4t_d0_y0u_m34n_1_C4Nt_jU5t_4dd_m0re_c03FFs?!??!?!????}