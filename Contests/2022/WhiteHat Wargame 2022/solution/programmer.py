from factordb.factordb import FactorDB
from Crypto.Util.number import *

enc = [604, 2170, 3179, 884, 1313, 3000, 1632, 884, 855, 3179, 119, 1632, 2271, 119, 612, 2412, 2185, 2923, 2412, 1632, 2271, 2271, 1313, 2412, 119, 3179, 119, 2170, 1632, 2578, 1313, 119, 2235, 2185, 119, 745, 3179, 1369, 1313, 1516]
n = 3233
e = 17

f = FactorDB(n)
f.connect()

p, q = f.get_factor_list()
d = inverse(e, (p - 1)*(q - 1))

flag = ""
for c in enc:
    char = chr(pow(c, d, n))
    flag += char 

print(flag)

# Flag: WhiteHat{i_am_programmer_i_have_no_life} 