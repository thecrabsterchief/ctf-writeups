# Halloweens_magix

## Solution

Đọc sơ qua thì bài này encrypt file **flag.png** bằng cách chuyển 16 bytes liên tiếp của flag thành một ma trận 4x4 sau đó nhân ma trận này với một ma trận `key` 4x4, mỗi thành phần là 1 số random trong đoạn [0, 64].

Đây là một bài khá dễ nếu chúng ta chú ý 2 điều sau:

* Kết quả của phép nhân là một ma trận 4x4 mà giá trị của mỗi ô tối đa là 4 * 64 * 256 (~ 2 bytes). Do đó lúc đọc file **flag.png.enc** ta cần đọc từng block `32 bytes`, mỗi `2 bytes` liên tiếp sẽ tưởng ứng với 1 ô trong ma trận 4x4

* Vì format của flag là **.png** nên ta biết được 16 bytes header của png và do đó ta dễ dàng tìm lại được key bằng cách nhân nghịch đảo ma trận header với ma trận đầu của output. Có key rồi dễ dàng decrypt toàn bộ phần còn lại.

Code mình để [ở đây](./sol.py)

## Flag

![flag](./flag.png)