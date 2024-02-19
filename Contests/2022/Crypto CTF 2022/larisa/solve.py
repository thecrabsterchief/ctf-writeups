from sage.all import *

l, e = 128, 65537
S = SymmetricGroup(l)
d = pow(e, -1, S.order())

if __name__ == "__main__":
  # recover `M`
  C = eval(open("./enc.txt", "r").read())  
  M = [
    list((S(c)**d).tuple()) for c in C
  ]

  # recover `flag``
  decrypt = lambda M, r, s: "".join([chr(m[(_*r + s)%l]) for _, m in enumerate(M)])
  for r in range(2, l):
    for s in range(2, l):
      flag = decrypt(M, r, s)
      if "CCTF{" in flag:
        print(flag, r, s)