from sage.all import *

# E: Y2 = E(X3 + 497 X + 1768, p: 9739
a, b, p = 497, 1768, 9739
E = EllipticCurve(GF(p), [a, b])

P = E((2339, 2213))
Q = 7863 * P

x, y = Q.xy()

print("crypto{" + str(x) + "," + str(y) + "}")
# Flag: crypto{9467,2742}