from pwn import *
from tqdm import tqdm

def parse(point):
    # (x : y : 1) -> (x, y)
    point = point[1:-5]
    return list(map(int, point.split(" : ")))


def gen():
    io.sendlineafter(b": ", b"1")
    io.recvuntil(b"p = "); p = int(io.recvline())
    io.recvuntil(b"P = "); P = parse(io.recvline().strip().decode())
    io.recvuntil(b"Q = "); Q = parse(io.recvline().strip().decode())
    return p, P, Q

def flag():
    io.sendlineafter(b": ", b"2")
    io.recvuntil(b"Secret is given to you: ")
    return int(io.recvline().decode().strip(), 16)

if __name__ == "__main__":
    data = []
    io = remote("vsc.tf", 3462)
    
    for _ in tqdm(range(32*624//256)):
        p, P, Q = gen()
        data.append([p, P, Q])
    ct = flag()
    io.close()

    with open("data.txt", "w") as file:
        file.write(f"data = {data}\n")
        file.write(f"ct = {ct}")