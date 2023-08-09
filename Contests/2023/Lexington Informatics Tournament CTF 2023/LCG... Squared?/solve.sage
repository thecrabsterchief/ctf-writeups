from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes as l2b
from Crypto.Util.Padding import pad

# x(n) = y(n-1)*x(n-1) + c  [mod p]
# y(n) = a*y(n-1) + b       [mod p]

Xs = [
    3157380704489980167,
    202791412938399925,
    705892353208348176,
    5062131254806651470,
    3846448923626044516
]
p = 11252070083876103037
iv = bytes.fromhex("e5b9ad12334f59c192818a1f03044b3d")
ct = bytes.fromhex("2d19c850490713b6019334c8fe1c8cc1fb0cf8f67deb9245763222784300598c1675b13f504b8178c3ed349b3978b05bfa61935ab4ce9427742442d64d85c6691b97c5b4d55c553ccb05b617a94e2a23")

PR.<a, b, c, x, y> = PolynomialRing(GF(p))

x0, y0 = x, y
I = []

for i in range(5):
    if i == 0:
        I.append(y0*x0 + c - Xs[i])
    else:
        I.append(y0*Xs[i-1] + c - Xs[i])

    y0 = a*y0 + b

I = PR.ideal(I)
B = I.groebner_basis()
fy = B[0].univariate_polynomial()

for _y, _ in fy.roots():
    _a = -B[1](y=_y, a=0)
    _b = -B[2](y=_y, b=0)
    _c = -B[3](y=_y, c=0)
    _x = -B[4](y=_y, x=0)

    y0 = _y
    l1 = lambda y: _a*y + _b 
    l2 = lambda x, y: y*x + _c 

    for i in range(5):  y0 = l1(y0)
    
    r = int(l2(Xs[-1], y0))
    k = pad(l2b(r**2), 16)
    cipher = AES.new(k, AES.MODE_CBC, iv=iv)
    print(cipher.decrypt(ct))