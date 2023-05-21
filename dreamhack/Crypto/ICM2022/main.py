import random
from fractions import Fraction


def enc(p, n, key1, key2):
    q = (Fraction(p, n+1)*key1**(n+1)) - (Fraction(p, n+1)*key2**(n+1))
    print("[OK] plain is encrypted : ", q)
    return q


def dec(q):
    # cencored


def key_make():
    n, key1, key2 = 0, 1, 0
    while key2 < key1:
        n = random.randrange(1, 10)
        key1 = random.randrange(1, 100)
        key2 = random.randrange(1, 100)
    return n, key1, key2


p = ""
emp = input("plain text: ")
for character in emp:
    p += str(ord(character))
n, key1, key2 = key_make()

print(f"[WAR]p = {p} n = {n} key1 = {key1} key2 = {key2}")

q = enc(int(p), n, key1, key2)
dec(q)
