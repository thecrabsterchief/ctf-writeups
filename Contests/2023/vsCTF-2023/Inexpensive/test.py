from sage.all import *
from Crypto.Cipher import AES
from Crypto.Util.number import *

def build_lattice(mat, lb, ub):
    n = mat.ncols()  # num equations
    m = mat.nrows()  # num variables
    if n != len(ub) or n != len(lb):
        raise ValueError("Number of equations must match number of bounds")
    if any([l > u for l, u in zip(lb, ub)]):
        raise ValueError("All lower bounds must be less than upper bounds")

    L = matrix(ZZ, mat)
    target = vector([(l + u) // 2 for u, l in zip(ub, lb)])

    bounds = [u - l for u, l in zip(ub, lb)]
    K = max(bounds) or L.det()
    Q = matrix.diagonal([K // x if x != 0 else K * n for x in bounds])
    return L, target, Q


def babai_cvp(mat, target, reduction=lambda M: M.LLL()):
    M = reduction(matrix(ZZ, mat))
    G = M.gram_schmidt()[0]
    diff = target
    for i in reversed(range(G.nrows())):
        diff -= M[i] * ((diff * G[i]) / (G[i] * G[i])).round()
    return target - diff


def kannan_cvp(mat, target, reduction=lambda M: M.LLL(), weight=None):
    if weight is None:
        weight = max(target)
    L = block_matrix([[mat, 0], [-matrix(target), weight]])
    for row in reduction(L):
        if row[-1] < 0:
            row = -row
        if row[-1] == weight:
            yield row[:-1] + target


def solve_inequality(M, lb, ub, cvp=kannan_cvp):
    L, target, Q = build_lattice(M, lb, ub)
    for vt in cvp(L * Q, Q * target):
        yield Q.solve_left(vt)

iv = '6f80a4db411283cbfc8c2f7520e65d28'
ct = '5f7b8a174d6c6639ba86a12d4bd4d540d72649d9291621408af19bb6c6ffe9accbb998f8b72f11bb44ec54cdfd9f104d742161caf46565bd0bdfa1408c4938259b71f40024bdb72f6a1cee21e9e4a8a6'
public = (5493730386557588740213129802259912244320687664566838908933139695297485450984, 112890332916025956487764670868844990362012495830331005756101957669156593225707)
s = 56275471718384662997548252167133434300653095757824127552821000258065614147953
r = 88763903751156737929684129280869308730236267295398468396864060901397400254458
msg = '79e3587b06b1caec3323a5f3b944b4946e06aedca38e2b0d6b231c4577a192bf'


p = 115792089237316195423570985008687907852837564279074904382605163141518161494337 # order
a = ZZ(s*2**128 - r)%p
b = ZZ(s - r*2**128)%p
W = 2**128
c = bytes_to_long(bytes.fromhex(msg))

B = matrix(ZZ, [
    [1, 0, 0,  a],
    [0, 1 ,0,  b],
    [0, 0, 1,  p],
])

ub = [2**128, 2**128, (c - 2**127*(a + b))//p, c]
lb = [2**127, 2**127, (c - 2**128*(a + b))//p, c]

for sol in solve_inequality(B, lb, ub):
    _x, _y = sol[:2]
    assert (a*_x + b*_y)%p == c
    d = int(_y*2**128 + _x)
    hd = hex(d)[2:]
    if len(hd) % 2 == 1:
        hd = '0' + hd
    key = bytes.fromhex(hd)
    cipher = AES.new(key, AES.MODE_CBC, iv=bytes.fromhex(iv))
    print(cipher.decrypt(bytes.fromhex(ct)))

# vsctf{Me_wen_i_need_256_random_bits_everytime_i_wanna_sign_smthng_:sadge:}