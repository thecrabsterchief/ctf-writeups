#!/usr/bin/env python3
from Crypto.Cipher import ARC4
from base64 import b64encode
import zlib
from secret import flag, key

file = {"flag.txt" : flag, "key" : key}

def print_menu():
    print("1. List file")
    print("2. Download file")
    print("3. Add file")
    print("4. Copy file")
    print("5. Remove File")
    print("6. Logout")

def download_file():
    filename = input("File name >> ").strip()
    if filename not in file:
        print("No such file")
        pass
    content = file[filename]
    rc4 = ARC4.new(key.encode())
    enc = rc4.encrypt(zlib.compress(file[filename].encode()))
    print("Content :", b64encode(enc).decode())

def get_filename():
    filename = input("File name >> ").strip()
    if filename == "key":
        print("No!")
        exit(0)
    return filename

def add_content(filename, content):
    if filename not in file:
        file[filename] = ""
    file[filename] += content

def remove_file(filename):
    if filename not in file:
        print("No such file")
    elif filename == "key":
        print("No!")
        exit(0)
    else:
        del file[filename]

print("Welcome to safe storage! Make sure to bring your key!")
while True:
    print_menu()
    ipt = input(">> ").strip()
    if ipt == "1":
        print(" ".join(file.keys()))
    elif ipt == "2":
        download_file()
    elif ipt == "3":
        filename = get_filename()
        add_content(filename, input("Content >>").strip())
    elif ipt == "4":
        origin = input("Which file to copy >> ").strip()
        filename = get_filename()
        add_content(filename, file[origin])
    elif ipt == "5":
        filename = input("Which file to remove >> ").strip()
        remove_file(filename)
    elif ipt == "6":
        break
