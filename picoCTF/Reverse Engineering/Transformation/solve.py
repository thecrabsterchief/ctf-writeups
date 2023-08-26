# ''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])

with open("./enc", "r") as f:
    enc = f.read()
    flag = []
    for c in enc:
        b = ord(c)
        flag.extend([b >> 8, b & 0xff])

    print(bytes(flag).decode())
