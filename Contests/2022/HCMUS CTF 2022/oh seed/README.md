# Oh seed

Đọc `source` thì đề sẽ sinh `random` 1 mảng gồm 666 số nguyên (32 bit) và leak cho ta 665 số đầu, nếu ta đoán được số cuối thì sẽ được `flag`. Bài này khá lạ với mình vì mọi thử có đều có vẻ `random` và mình chưa thấy sự liên kết gì.

Sau một hồi tìm hiểu thì mình biết được hàm `random` trong `Python` dùng [Mersenne twister](https://en.wikipedia.org/wiki/Mersenne_Twister) làm `pseudorandom number generator`. Từ đó nếu mình biết được đủ nhiều các giá trị thì sẽ hoàn toàn reverse được hàm random (mình có tham khảo code [ở đây](https://github.com/eboda/mersenne-twister-recover))

**`FLag: HCMUS-CTF{r4nd0m-1s-n0t-r4nd0m}`**