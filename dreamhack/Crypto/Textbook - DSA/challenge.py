from Crypto.Util.number import getPrime, inverse, bytes_to_long, isPrime
from random import randrange, choices
from hashlib import sha1
import string


class DSA(object):
    def __init__(self):
        while True:
            self.q = getPrime(160)
            r = randrange(1 << 863, 1 << 864)
            self.p = self.q * r + 1
            if self.p.bit_length() != 1024 or isPrime(self.p) != True:
                continue
            self.g = pow(2, r, self.p)
            if self.g == 1:
                continue
            self.x = randrange(1, self.q)
            self.y = pow(self.g, self.x, self.p)
            self.k = inverse(self.x, self.q)
            break

    def sign(self, msg):
        r = pow(self.g, self.k, self.p) % self.q
        h = bytes_to_long(sha1(msg).digest())
        s = inverse(self.k, self.q) * (h + self.x * r) % self.q
        return (r, s)

    def verify(self, msg, sig):
        r, s = sig
        if s == 0:
            return False
        s_inv = inverse(s, self.q)
        h = bytes_to_long(sha1(msg).digest())
        e1 = h * s_inv % self.q
        e2 = r * s_inv % self.q
        r_ = pow(self.g, e1, self.p) * pow(self.y, e2, self.p) % self.p % self.q
        if r_ == r:
            return True
        else:
            return False


dsa = DSA()
token = "".join(choices(string.ascii_letters + string.digits, k=32)).encode()

print("Welcome to dream's DSA server")
while True:
    print("[1] Sign")
    print("[2] Verify")
    print("[3] Get Info")

    choice = input()

    if choice == "1":
        print("Input message (hex): ", end="")
        msg = bytes.fromhex(input())
        if msg == token:
            print("Do not cheat !")
        else:
            print(dsa.sign(msg))

    elif choice == "2":
        print("Input message (hex): ", end="")
        msg = bytes.fromhex(input())
        if len(msg) > 100:
            print("Too long message")
        else:
            print("Input signagure (r, s as decimal integer): ", end="")
            sig = map(int, input().split(", "))
            if dsa.verify(msg, sig) == True:
                print("Signature verification success")
                if msg == token:
                    print(open("flag", "rb").read())
            else:
                print("Signature verification failed")

    elif choice == "3":
        print(f"p = {dsa.p}")
        print(f"q = {dsa.q}")
        print(f"g = {dsa.g}")
        print(f"y = {dsa.y}")
        print(f"token = {token}")

    else:
        print("Nope")
