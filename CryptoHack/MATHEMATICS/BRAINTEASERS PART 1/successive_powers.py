from sage.all import *

A = [588, 665, 216, 113, 642, 4, 836, 114, 851, 492, 819, 237]
p = max(A)

while p < 1000:
    p = next_prime(p)
    F = GF(p)
    X = set([F(A[i + 1])/F(A[i]) for i in range(len(A) - 1)])
    
    if len(X) == 1:
        print(p, X.pop())
        exit()