# transposition-trial
## Challenge

Đọc file `message.txt` và mô tả đề bài thì có vẻ `plaintext` đã bị xáo trộn theo từng `block` có độ dài bằng 3. Hmm... 2 từ đầu tiên sau khi sắp xếp lại có vẻ là `The flag...` từ đây mình thấy được mỗi `block` sẽ đưa kí tự cuối cùng ra trước (vd: `ABC` thành `CAB`) từ nhận xét đó mình tìm được flag :D

## Solution
```py
ciphertext = open('message.txt', 'r').read()

message = ""

for i in range(0, len(ciphertext), 3):
    message += ciphertext[i + 2] + ciphertext[i:i + 2]

print(message)
```

## Flag
**`picoCTF{7R4N5P051N6_15_3XP3N51V3_A9AFB178}`**