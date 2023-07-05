# DCeased-XXIV

## Solution

Đề cho ta 3 file:

* `part.png`: file flag chỉ bị encrypt phần sau, một số phần đầu vẫn chưa encrypt.

* `out.png` : flag bị encrypt hoàn toàn.

* `enc.py`: chứa thuật toán encrypt, đại khóa là xor từng pixel của flag với một số random nào đó.

Mới đâu chắc mọi người đều nghĩ tới `exiftool out.png => brute timestamp` nhưng điều đáng ngờ ở bài này là mình lại được biết đoạn đầu của flag, điều này có nghĩa là mình sẽ biết được một số các output của hàm random. Và vì hàm random trong python là [Mersenne Twister](https://en.wikipedia.org/wiki/Mersenne_Twister) nên nếu biết được 624 output thì hoàn toàn có thể predict được cái output tiếp theo, biết được toàn bộ key ta hoàn toàn có thể tìm lại flag!

Code mình để [ở đây](./sol.py)

## Flag

![flag](./FLAG.png)
