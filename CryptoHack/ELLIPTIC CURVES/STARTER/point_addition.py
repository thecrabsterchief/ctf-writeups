from sage.all import *

# E: Y2 = E(X3 + 497 X + 1768, p: 9739
a, b, p = 497, 1768, 9739
E = EllipticCurve(GF(p), [a, b])

P = E((493, 5564))
Q = E((1539, 4742))
R = E((4403,5202))
S = P + P + Q + R

x, y = S.xy()
print("crypto{" + str(x) + "," + str(y) + "}")
# Flag: crypto{4215,2162}