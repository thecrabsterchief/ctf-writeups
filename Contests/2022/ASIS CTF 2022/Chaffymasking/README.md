## Chaffymasking

## Description

Chaffy masking is a popular cryptography technique that is used to protect cryptographic implementations against several attacks.

## Solution

Đại khái bài này mình nhập vô một chuỗi bất kì sau đó nó sẽ kiểm tra và pad cái chuỗi mình nhập cho đủ 128 bytes. Tiếp theo nó chia cái chuỗi làm 2 phần bằng nhau và thực hiện hàng loạt các bước tính toán để sinh ra 2 vector key1 và key2, cuối cùng kết quả trả về sẽ là flag xor key1 xor key2.

Điều "bất thường" ở bài này là nếu ta nhập chuỗi ban đầu có độ dài đúng bằng 128 và khi chia chuỗi đó làm đôi thì ta được 2 chuỗi khác nhau. Lúc này ta sẽ loại bỏ được các phần random padding lúc check length mà hoàn toàn tự implement để gen ra hai cái key1 và key2 lúc này chỉ việc xor ngược lại là ra flag thôi =))

Code mình để [ở đây](./sol.py)

**FLag: ASIS{Lattice_based_hash_collision_it_was_sooooooooooooooo_easY!}**