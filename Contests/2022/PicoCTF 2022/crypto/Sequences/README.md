# Sequences

## Challenge

Mục tiêu chính của bài này là tính giá trị `m_func(k)` với `k = int(2e7)`. Tất nhiên chúng ta không cứ để đó mà chạy vì sẽ bị `tràn Stack`. Bài ta sẽ dùng một chút kiến thức đại số tuyến tính cụ thể là chéo hóa ma trận. Các bạn có thể tham khảo ví dụ kinh điển về tính dãy `Fibonacci` bằng ma trận tại [đây](https://www.geeksforgeeks.org/matrix-exponentiation/)

Vậy đầu tiên ta viết lại công thức truy hồi của dãy ban đầu về dạng mà trận và đi chéo hóa:

Từ đây ta thấy số hạng tổng quát của dãy sẽ có dạng: `f_n = a*12^n + b*13^n + c*(-21)^n + d*17^d`. Có sẵn `f_0, f_1, f_2, f_3` nên dễ dàng tính được `a, b, c, d` từ đó có được công thức tổng quát ==> xong!!!

## Solution
```py
import hashlib
import sys

a, b, c, d, m = 981920, -1082829, 1612, 141933, 42636
k, mod = int(2e7), 10**10000
sol = ( ( a*pow(12, k) + b*pow(13, k) + c*pow(-21, k) + d*pow(17, k) ) // m ) % mod

VERIF_KEY = "96cc5f3b460732b442814fd33cf8537c"
ENCRYPTED_FLAG = bytes.fromhex("42cbbce1487b443de1acf4834baed794f4bbd0dfe7d7086e788af7922b")

def decrypt_flag(sol):
    sol = sol % (10**10000)
    sol = str(sol)
    sol_md5 = hashlib.md5(sol.encode()).hexdigest()

    if sol_md5 != VERIF_KEY:
        print("Incorrect solution")
        sys.exit(1)

    key = hashlib.sha256(sol.encode()).digest()
    flag = bytearray([char ^ key[i] for i, char in enumerate(ENCRYPTED_FLAG)]).decode()

    print(flag)

decrypt_flag(sol)
```
# Flag
**`picoCTF{b1g_numb3rs_3956e6c2}`**