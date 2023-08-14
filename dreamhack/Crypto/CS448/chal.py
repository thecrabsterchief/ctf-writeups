#!/usr/bin/python3
import os, sys
import struct

def _print(content, end = None):
    if end != None:
        print(content, end = end)
    else:
        print(content)
    sys.stdout.flush()

def read_flag():
    with open("flag", "r") as f:
        res = f.read()
    return res

def print_prompt():
    _print("1. encrypt input")
    _print("2. decrypt input")
    _print("3. encrypt flag")
    _print("4. exit")
    _print(">> ", end = "")

def read_int():
    return int(read_string())

def read_string():
    return input().strip()

def get_random_u8():
    return struct.unpack("<B", os.urandom(1))[0]

def encrypt(s, k):
    res = ""
    if k <= len(s):
        _print("[!] key shold be larger then len(pt) for safty!!")
        return ""
    for i, c in enumerate(s):
        enc = (get_random_u8() + k * i) % 0xff
        enc = ord(c) ^ enc
        res += hex(enc)[2:].rjust(2, "0")
    return res

def decrypt(s, k):
    _print("[*] Give me the paper about predicting urandom")
    _print("[*] ...Then i'll decrypt your input ;)")
    return ""

if __name__ == "__main__":
    flag = read_flag()
    while True:
        print_prompt()
        c = read_int()
        if c == 1:
            _print("key >> ", end = "")
            key = read_int()
            _print("pt >> ", end = "")
            pt = read_string()
            _print("result : %s"%encrypt(pt, key))
        elif c == 2:
            _print("key >> ", end = "")
            key = read_int()
            _print("ct >> ", end = "")
            ct = read_string()
            _print("result : %s"%decrypt(ct, key))
        elif c == 3:
            _print("key >> ", end = "")
            key = read_int()
            _print("result : %s"%encrypt(flag, key))
        elif c == 4:
            _print("bye!!")
            exit(0)
        else:
            _print("invalid option...")
