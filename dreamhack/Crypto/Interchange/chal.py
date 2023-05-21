#!/usr/bin/python3
import os
from cipher import *

def read_flag():
    with open("flag", "r") as f:
        flag = f.read()
    return flag

def print_prompt(e):
    print("[*] Current Encryptor : %s" % e)
    print("--------------------------------")
    print("1. Encrypt input")
    print("2. Encrypt flag")
    print("3. Switch the encryptor")
    print("4. Exit")
    print(">> ", end = "")

def read_int():
    return int(read_string())

def read_string():
    return input().strip()

def init_encryptor():
    key = os.urandom(BS)
    return (CBC_cipher(key), CTR_cipher(key), OFB_cipher(key))

if __name__ == "__main__":
    FLAG = read_flag()
    encryptor_li = list(init_encryptor())

    while True:
        print_prompt(encryptor_li[0])
        c = read_int()
        if c == 1:
            print("[*] pt >> ", end = "")
            pt = read_string()
            ct = encryptor_li[0].encrypt(pt)
            print("[+] ct : %s"%ct.hex())
        elif c == 2:
            ct = encryptor_li[0].encrypt(FLAG)
            print("[+] Encrypted flag : %s"%ct.hex())
        elif c == 3:
            encryptor_li = encryptor_li[1:] + encryptor_li[:1]
            print("[+] Successfully Switched!!")
        elif c == 4:
            print("[*] Thank you for usage~")
            exit(0)
        else:
            print("[?] invalid option :?")


