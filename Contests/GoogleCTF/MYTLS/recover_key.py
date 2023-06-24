from hashlib import sha256
from string import printable as table

key_len = 241
leak = open("./log.txt", "r").read().split("\n")
recovered = ""

for i in reversed(range(key_len)):
    for char in table:
        suffix = char.encode() + recovered.encode()
        if sha256(b"1"*i + suffix).hexdigest() == leak[i]:
            recovered = char + recovered
            break

print(recovered)

with open("./server-ecdhkey.pem", "r") as f:
    f.write(recovered)

print("run get_flag.py")