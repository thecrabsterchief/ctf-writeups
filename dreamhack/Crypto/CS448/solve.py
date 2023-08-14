from pwn import *
from tqdm import tqdm

def get():
    io.sendlineafter(b">> ", b"3")
    io.sendlineafter(b">> ", b"255")
    io.recvuntil(b" : ")
    return bytes.fromhex(io.recvline().decode().strip())

# io = process(["python3", "chal.py"])
io = remote("host3.dreamhack.games", 14626)

len_flag = len(get())
vote = [[0 for j in range(256)] for i in range(len_flag)]

for _ in tqdm(range(11000)):
    ct = get()
    for i, b in enumerate(ct):
        vote[i][b] += 1


    if (_ + 1)%256 == 0:
        flag = []
        for v in vote:
            _v = v[32:127]
            flag += [_v.index(max(_v)) + 32]

        print(bytes(flag))
