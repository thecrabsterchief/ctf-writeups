# nanoDiamond

![nano1](../_img/nano1.png)

Mình sẽ nói sơ qua đề bài: ở mỗi round sẽ có 1 mảng 6 phần tử mang giá trị True, False chưa biết, và đề cho ta 14 lần để tính giá trị luận lý của 6 phần tử bí mật đó, biết rằng trong 14 lần test có tối đa 2 lần mà kết quả trả về sai với thực tế. Nếu sau 14 lần ta đoán được chính xác 6 phần tử bí mật thì sẽ pass qua round đấu, vượt hết 50 round thì sẽ có flag.

Ý tưởng của mình là check (Bi == 1) 2 lần (tổng cộng hết 12 lần test), nếu cả hai lần đều ra cùng kết quả thì "khả năng cao" ta biết được luôn giá trị của Bi, còn nếu kết quả khác nhau (tối đa chỉ có 2 vì tối đa có 2 trong 14 lần kết quả trả về sai với thực tế). Lúc này ta dùng 2 lần còn lại đễ check tiếp sau cho tăng độ chính xác lên... Và sau 15p mình cũng lấy được flag (code mình chạy vài lần thì đa số pass được trên 30 round nên mình để vậy luôn rồi coi bài khác mà không tìm cách tốt hơn... khá tin... vào nhân phẩm :v)

```python
import string
import secrets
from hashlib import sha256
from random import randint, shuffle, choice
from pwn import *

ROUND_NUM = 50
PREROUND_NUM = 14
CHEST_NUM = 6

white_list = ['==','(',')','0','1','and','or','B0','B1','B2','B3','B4','B5']


def proof_of_work():
    ltt = string.digits + string.ascii_letters
    data = io.recvline()[:-1].decode()
    hash = data.split(" == ")[1]
    suffix = data.split("+")[1][:16]
    for a in ltt:
        for b in ltt:
            for c in ltt:
                for d in ltt:
                    secret = a + b + c + d + suffix
                    if sha256(secret.encode()).hexdigest() == hash:
                        print(f'[+] Proof of work done! Secret is {secret}')
                        io.recvuntil(b"Give me XXXX: ")
                        io.sendline((a + b + c + d).encode())

def check(i):
    io.recvuntil(b'Question: ')
    io.sendline(f'B{i} and 1'.encode())
    ans = io.recvline()
    if b'True' in ans:
        return 1
    return 0

def round(i):
    print(f'Round {i}')
    io.recvline()
    io.recvline()
    io.recvline()

    chest1 = [] 
    for i in range(6):
        chest1.append(check(i))

    chest2 = [] 
    for i in range(6):
        chest2.append(check(i))
    
    chest = chest1
    wrindex = []
    for i in range(6):
        if chest1[i] != chest2[i]:
            wrindex.append(i)
    
    if len(wrindex) == 0:
        for i in range(2):
            check(i)
    
    elif len(wrindex) == 1:
        ii = wrindex[0]
        check(0)
        chest[ii] = check(ii)
    else:
        for i in wrindex:
            chest[i] = check(i)
    
    io.recvuntil(b'Now open the chests:')
    io.sendline(' '.join(str(x) for x in chest).encode())
    print(io.recvline())

io = remote("1.13.154.182", 33863)
proof_of_work()

print(io.recvline())
print(io.recvline())

for i in range(50):
    round(i)

print(io.recvline())
print(io.recvline())

# Flag: WMCTF{TERR4R1a_IS_4_LAND_0F_@DVENturE}
```

**Flag: WMCTF{TERR4R1a_IS_4_LAND_0F_@DVENturE}**