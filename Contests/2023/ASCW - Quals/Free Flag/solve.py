from pwn import p64

def sub_77A(a1, a2):
    out = (a1 << a2) | (a1 >> (-a2 & 7))
    return out & 0xff

v8 = [
    0x26666FE8EA686A28, 0xAEE8EBE666666666, 0xEBA5EB4E666E6E66, 0xAFA5
]
v8 = b"".join(p64(i) for i in v8)

flag = [
    sub_77A(i, 3) for i in v8 
]
print(bytes(flag))
