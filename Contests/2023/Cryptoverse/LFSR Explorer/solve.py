def int2list(n):
    return list(map(int, bin(n)[2:].zfill(32)))

def solve(output):
    state = output
    taps  = int2list(0b10000100010010001000100000010101)
    for o in output[::-1]:
        state = [
            (o - sum(s*t for s,t in zip(state[:-1], taps[1:]))) % 2
        ] + state[:-1]
    return state

with open("./output.txt", "rb") as f:
    output = f.read()

flag  = solve(int2list(int.from_bytes(output[4:], 'big')))
flag += solve(int2list(int.from_bytes(output[:4], 'big')))
flag  = b"cvctf{" + int.to_bytes(
    int("".join(str(f) for f in flag), 2), length=8, byteorder='big'
) + b"}"

print(flag)