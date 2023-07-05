import hashlib
from Crypto.Util.number import *
from random import randint
from os import urandom
from base64 import b64decode, b64encode
from hashlib import sha256

with open("../flag.txt") as file:
    FLAG = file.read()

class SignatureScheme:
    def __init__(self) -> None:
        self.N = len(FLAG)
        assert self.N == 32

        self.p = 99489312791417850853874793689472588065916188862194414825310101275999789178243
        self.x = randint(1, self.p - 1)
        self.g = randint(1, self.p - 1)
        self.y = pow(self.g, self.x, self.p)
        self.coef = [randint(1, self.p - 1) for _ in range(self.N)]

        self.sign_attempt = self.N

    def sign(self, pt):
        if self.sign_attempt == 0:
            print("Sorry, no more attempt to sign")
            return (0, 0)
        else:
            try:
                msg = b64decode(pt)
                
                if (len(msg) > self.N): # I know you are hecking :(((
                    return (0, 0)
                
                k = sum([coef * m for coef, m in zip(self.coef, msg)])
                if k % 2 == 0: # Just to make k and p-1 coprime :)))
                    k += 1
                
                r = pow(self.g, k, self.p)
                h = bytes_to_long(sha256(pt).digest())
                s = ((h - self.x * r) * inverse(k, self.p - 1)) % (self.p - 1)
                self.sign_attempt -= 1
                return (r, s)
            except:
                print('Please send message in base64 encoding')

    def verify(self, pt, r, s):
        if not 0 < r < self.p:
            return False
        if not 0 < s < self.p - 1:
            return False
        h = bytes_to_long(sha256(pt).digest())
        return pow(self.g, h, self.p) == (pow(self.y, r, self.p) * pow(r, s, self.p)) % self.p   

    def get_flag(self):
        try:
            test = b64encode(urandom(self.N))
            print("Could you sign this for me: ", test.decode())
            r = b64decode(input('Input r: '))
            s = b64decode(input('Input s: '))
            if self.verify(test, bytes_to_long(r), bytes_to_long(s)):
                print("Congratulation, this is your flag: ", FLAG)
                exit(0)
            else:
                print("Sorry, that is not my signature")
                exit(-1)
        except Exception as e:
            print(e)
            print("Please send data in base64 encoding")

    def menu(self):
        print(f"You have only {self.sign_attempt} attempts left")
        print("0. Get public key")
        print("1. Sign a message")
        print("2. Verify a message")
        print("3. Get flag")
        return int(input('Select an option: '))

    def main(self):
        print("Welcome to our sign server")
        while True:
            option = self.menu()

            if option == 0:
                print("g =", self.g)
                print("p =", self.p)
            elif option == 1:
                msg = input("Input message you want to sign: ").encode()
                r, s = self.sign(msg)
                print("Signature (r, s): ", (r, s))

            elif option == 2:
                msg = input('Your message: ').encode()
                r = b64decode(input('Input r: '))
                s = b64decode(input('Input s: '))
                if self.verify(msg, bytes_to_long(r), bytes_to_long(s)):
                    print("Valid signature")
                else:
                    print("Invalid signature")

            elif option == 3:
                self.get_flag()

            else:
                print("Stay away you hecker :(((")

c = SignatureScheme()
c.main()