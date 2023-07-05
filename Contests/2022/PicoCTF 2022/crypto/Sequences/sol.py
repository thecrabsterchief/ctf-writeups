import hashlib
import sys

a, b, c, d, m = 981920, -1082829, 1612, 141933, 42636
k, mod = int(2e7), 10**10000
sol = ( ( a*pow(12, k) + b*pow(13, k) + c*pow(-21, k) + d*pow(17, k) ) // m ) % mod

VERIF_KEY = "96cc5f3b460732b442814fd33cf8537c"
ENCRYPTED_FLAG = bytes.fromhex("42cbbce1487b443de1acf4834baed794f4bbd0dfe7d7086e788af7922b")

def decrypt_flag(sol):
    sol = sol % (10**10000)
    sol = str(sol)
    sol_md5 = hashlib.md5(sol.encode()).hexdigest()

    if sol_md5 != VERIF_KEY:
        print("Incorrect solution")
        sys.exit(1)

    key = hashlib.sha256(sol.encode()).digest()
    flag = bytearray([char ^ key[i] for i, char in enumerate(ENCRYPTED_FLAG)]).decode()

    print(flag)

decrypt_flag(sol)

# 'picoCTF{b1g_numb3rs_3956e6c2}'

#flag: picoCTF{b1g_numb3rs_3956e6c2}