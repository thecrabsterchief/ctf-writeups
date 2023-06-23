from sage.all import *
from hashlib import sha1

# E: Y2 = E(X3 + 497 X + 1768, p: 9739
a, b, p = 497, 1768, 9739
E = EllipticCurve(GF(p), [a, b])

Q  = E((815, 3190))
nb = 1829
x  = (nb * Q).xy()[0]

print("crypto{" + sha1(str(x).encode()).hexdigest() + "}")
# Flag: crypto{80e5212754a824d3a4aed185ace4f9cac0f908bf}