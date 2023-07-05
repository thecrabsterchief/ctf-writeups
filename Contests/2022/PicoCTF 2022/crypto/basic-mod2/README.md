# basic-mod2
## Challenge

Cũng tương tự như bài `basic-mod1` ta cũng có các quy tắc chuyển từng số trong file `message.txt` về dạng kí tự nhưng lần này phép biến đổi là **nghịch đảo modulos 41** thay vì phép **mod 37** như trước.

## Solution
```py
import string

letter = string.ascii_lowercase + string.digits + '_'

f = open('message.txt', 'r').read()
ciphertext = list(int(num) for num in f.split())

flag = ''.join(letter[pow(num, -1, 41) - 1] for num in ciphertext)

print('picoCTF{' + flag + '}')
```
## Flag
**`picoCTF{1nv3r53ly_h4rd_8a05d939}`**