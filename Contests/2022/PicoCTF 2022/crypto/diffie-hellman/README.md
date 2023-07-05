# diffie-hellman

## Challenge

Đây là bài liên quan đến hệ mã [Diffie–Hellman](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange). Đầu tiên ta tìm `shared secret key` của `Alice` và `Bob`: `key = pow(g, a*b, p)`, dùng `key` vừa tìm được để giải mã y hệt như bài `basic-mod` ta làm hồi nãy =)).

## Solution
```py
import string

letters = string.ascii_uppercase + string.digits

ciphertext = open("message.txt", 'r')
a, b, g, p = 7, 3, 5, 13

key, mod = pow(g, a*b, p), len(letters)

flag = ""

for char in ciphertext:
    if char in letters:
        flag += letters[(letters.index(char) - key) % mod]
    
    else:
        flag += char

print("picoCTF{" + flag + "}")
```
## Flag
**`picoCTF{C4354R_C1PH3R_15_4_817_0U7D473D_3A2BF44E}`**