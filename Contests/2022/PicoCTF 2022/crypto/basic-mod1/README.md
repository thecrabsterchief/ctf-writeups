# basic-mod1
## Challenge


Bài đầu tiên khá đơn giản, file `message.txt` chứa dãy các số nguyên. Công việc của ta đơn giản là lấy từng số nguyên `mod` cho `37`, khi đó nếu kết quả:
* Từ `0` đến `25`: đổi sang kí tự in hoa tương ứng
* Từ `26` đến `35`: đổi sang chữ số tương ứng
* Bằng `36`: đổi sang kí tự `underscore`
## Solution
```py
# Author: vnc1106

import string
letter = string.ascii_uppercase + string.digits + '_'

f = open('message.txt', 'r').read()
ciphertext = list(int(num) for num in f.split())

flag = ''.join(letter[num % 37] for num in ciphertext)

print('picoCTF{' + flag + '}')
```
## Flag
**`picoCTF{R0UND_N_R0UND_ADD17EC2}`**
