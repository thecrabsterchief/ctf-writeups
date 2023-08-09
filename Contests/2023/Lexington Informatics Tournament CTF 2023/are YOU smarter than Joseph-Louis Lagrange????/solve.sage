from Crypto.Util.number import *

Cs = [1825147270203874538950085, 1755355241290944436019489,  150220311113190713333212, 1826562141290875830948785]
Ys = matrix(ZZ, [
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [1, 0, 1, 0],
    [0, 1, 0, 1]
]).solve_right(vector(Cs))
print(Ys)
a,b,c,d = Ys
Xs = [i + 1 for i in range(4)]

PR.<x> = PolynomialRing(QQ)

fx = PR.lagrange_polynomial([
    (x, y) for x, y in zip(Xs, Ys)
])

assert fx(1) == a and fx(2) == b and  fx(3) == c and fx(4) == d
 
flag = Ys.list() + [fx(5)]
flag = "".join(str(x) for x in flag)
print(fx(5))

110006170013060408131904
1715141100190814130818181
40214141100130305201308
111421041100061700130604
6954957548549661084455388