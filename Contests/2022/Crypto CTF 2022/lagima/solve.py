from sage.all import *
from Crypto.Util.number import *

n = 313
S = SymmetricGroup(n)

if __name__ == "__main__":
  with open("./output.txt", "r") as f:
    G = eval(f.readline()[4:])
    H = eval(f.readline()[4:])
  
  x = crt(
    [discrete_log(S(h), S(g)) for h, g in zip(H, G)],
    [S(g).order() for g in G]
  )
  print(long_to_bytes(x))