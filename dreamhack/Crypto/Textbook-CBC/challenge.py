from Crypto.Util.Padding import pad, unpad
from random import choices, randint
from Crypto.Cipher import AES

BLOCK_SIZE = 16
flag = open("flag", "rb").read()
key = bytes(randint(0, 255) for i in range(BLOCK_SIZE))

encrypt = lambda pt: AES.new(key, AES.MODE_CBC, key).encrypt(pad(pt, BLOCK_SIZE))
decrypt = lambda ct: unpad(AES.new(key, AES.MODE_CBC, key).decrypt(ct), BLOCK_SIZE)

print("Welcome to dream's AES server")
while True:
    print("[1] Encrypt")
    print("[2] Decrypt")
    print("[3] Get Flag")

    choice = input()

    if choice == "1":
        print("Input plaintext (hex): ", end="")
        pt = bytes.fromhex(input())
        print(encrypt(pt).hex())

    elif choice == "2":
        print("Input ciphertext (hex): ", end="")
        ct = bytes.fromhex(input())
        print(decrypt(ct).hex())

    elif choice == "3":
        print(f"flag = {encrypt(flag).hex()}")
        exit()

    else:
        print("Nope")
