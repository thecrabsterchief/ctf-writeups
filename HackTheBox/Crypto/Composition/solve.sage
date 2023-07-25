#!/usr/local/bin/sage

from gmpy2 import *
from hashlib import md5
from Crypto.Cipher import AES 
from Crypto.Util.Padding import unpad

def fermat_factorize(N):
    # N = a^2 - b^2
    a  = iroot(N, 2)[0]
    b2 = a*a - N

    while b2 < 0 or not iroot(b2, 2)[1]:
        a += 1
        b2 = a*a - N
    
    b = iroot(b2, 2)[0]
    return a - b, a + b

def recover_curve(N, P, Q):
    # y^2 = x^3 + ax + b
    x1, y1 = P
    x2, y2 = Q
    return matrix(Zmod(N), [
        [x1, 1],
        [x2, 1]
    ]).solve_right(vector(Zmod(N), [y1**2 - x1**3, y2**2 - x2**3]))

ct = bytes.fromhex("d8b1aee35e1039facc02b778da8bb55be5ea700246dce1b3ef806170a857129620f4d4d944278a3e3aa21354376e227cc427f1082806074aa4a81a91e60c6e54")
iv = bytes.fromhex("8182efc3cc68e28104fd822f8e81f243")
N  = 11074738997974009388896578172530723220837450248455862095654602299571826580500309477214551846168283856777560899078868039753444371487410629333097512795512953
P = (9656027891181691861296995023135555098187739711023291681744887889475095424813816731076560432137643926325024603013036010151226496107827249933633564330071410, 9375168698463839046064050521985546982533063961771115249342823174640210020713233296796080809252720562142871709998469663582591452235376313074013106522181249)
H = (3625947512107982220576649118615342130682361756170314896244235061718080524825322135998727327928326620569493901132585872368525656195932154459216222449239361, 8869907512145443416545623156194716163657976166200058028161604091659848646707819033739578602065108724923776137720994218984173387537418000871401302581555520)


if __name__ == "__main__":
    p, q = fermat_factorize(N)
    e = next_prime(p >> (512 // 4))
    
    a, b = recover_curve(N, P, H)
    Ep = EllipticCurve(GF(p), [a, b])
    Eq = EllipticCurve(GF(q), [a, b])
    E  = EllipticCurve(Zmod(N), [a, b])

    np, nq = Ep.order(), Eq.order()
    d = crt(
        [pow(e, -1, np), pow(e, -1, nq)],
        [np, nq]
    )

    G = d * E.point(P)
    key = md5(str(G.xy()[0]).encode()).digest()
    cipher = AES.new(key,AES.MODE_CBC,iv)
    flag = unpad(cipher.decrypt(ct), 16).decode()
    print("Flag:", flag)