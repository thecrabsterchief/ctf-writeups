from sage.all import *
from randcrack import RandCrack # https://github.com/tna0y/Python-random-module-cracker/tree/master
from tqdm import tqdm
from Crypto.Util.number import *

def recover_curve(P, Q, p):
    # y^2 = x^3 + ax + b [mod p]
    a, b = matrix(GF(p), [
        [P[0], 1],
        [Q[0], 1]
    ]).solve_right(vector(GF(p), [
        P[1]**2 - P[0]**3,
        Q[1]**2 - Q[0]**3
    ]))

    return EllipticCurve(GF(p), [a, b])

def smart_attack(P,Q,p):
    E = P.curve()
    Eqp = EllipticCurve(Qp(p, 2), [ ZZ(t) + randint(0,p)*p for t in E.a_invariants() ])

    P_Qps = Eqp.lift_x(ZZ(P.xy()[0]), all=True)
    for P_Qp in P_Qps:
        if GF(p)(P_Qp.xy()[1]) == P.xy()[1]:
            break

    Q_Qps = Eqp.lift_x(ZZ(Q.xy()[0]), all=True)
    for Q_Qp in Q_Qps:
        if GF(p)(Q_Qp.xy()[1]) == Q.xy()[1]:
            break

    p_times_P = p*P_Qp
    p_times_Q = p*Q_Qp

    x_P,y_P = p_times_P.xy()
    x_Q,y_Q = p_times_Q.xy()

    phi_P = -(x_P/y_P)
    phi_Q = -(x_Q/y_Q)
    k = phi_Q/phi_P
    return ZZ(k)

if __name__ == "__main__":
    rc = RandCrack()
    data, ct = [], 0
    N = 32*624//256
    exec(open("./data.txt", "r").read())
    for _ in tqdm(range(N)):
        p, P, Q = data[_]
        E = recover_curve(P, Q, p)
        s256 = smart_attack(E(P), E(Q), p)
        s256 = bin(s256)[2:].zfill(256)
        s32 = [int(s256[i:i+32], 2) for i in range(0, 256, 32)]
        for s in s32[::-1]:
            rc.submit(s)

    a, b = [rc.predict_getrandbits(1337) for _ in '01']
    m = (ct - b)//a
    print(long_to_bytes(m))

# vsctf{randomization_is_not_too_fancy_because_you_are_Smart!}