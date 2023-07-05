# credstuff

## Challenge

Đề cho ta hai file `usernames.txt` và tương ứng là `passwords.txt`, mục tiêu là tìm password của user `cultiris` sẽ chứa thông tin mã hóa của `flag`

**Bước 1:** Tìm password
```py
User = open('usernames.txt', 'r').read().split('\n')
Pass = open('passwords.txt', 'r').read().split('\n')

Accounts = {u:p for (u, p) in zip(User, Pass)}

ciphertext = Accounts['cultiris']
```
Ta tìm được pass là: `cvpbPGS{P7e1S_54I35_71Z3}`

**Bước 2:** Giải mã password
Nhìn qua là biết đây là mã `Caesar`, chú ý format của `flag` là `picoCTF{}` nên ta tính được `key = (ord('c') - ord('p')) % 26` từ đó dễ dàng tìm được `flag`

## Solution
```py
from string import *

User = open('usernames.txt', 'r').read().split('\n')
Pass = open('passwords.txt', 'r').read().split('\n')

Accounts = {u:p for (u, p) in zip(User, Pass)}

ciphertext = Accounts['cultiris']

key = (ord(ciphertext[0]) - ord('p')) % 26

flag = ""

for char in ciphertext:
    if char in ascii_lowercase:
        flag += ascii_lowercase[(ascii_lowercase.index(char) + key) % 26]

    elif char in ascii_uppercase:
        flag += ascii_uppercase[(ascii_uppercase.index(char) + key) % 26]

    else:
        flag += char

print(flag)
```
## Flag
**`picoCTF{C7r1F_54V35_71M3}`**
