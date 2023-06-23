from sage.all import *

# E: Y2 = X3 + 497 X + 1768, p: 9739
a, b, p = 497, 1768, 9739
E = EllipticCurve(GF(p), [a, b])

P = E.point((8045,6936))
Q = -P
x, y = Q.xy()

print("crypto{" + str(x) + "," + str(y) + "}")
# Flag: crypto{8045,2803}