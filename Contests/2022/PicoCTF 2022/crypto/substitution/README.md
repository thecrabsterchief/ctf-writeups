# substitution
## Challenge
Ta gặp liên tiếp 3 bài đều là **substitution cipher**,  khác với mã **Caesar**, chỉ có **26** trường hợp khác nhau của **key** nên để phá mã chỉ việc **brute-force**. **Substitution cipher** có tới **26!** khả năng khác nhau và do đó ta không thể **brute-force** được. 

Để phá mã chúng ta sẽ dùng kĩ thuật kiểm tra tần suất xuất hiện của các chữ cái ([Frequency analysis](https://en.wikipedia.org/wiki/Frequency_analysis)). Ta chỉ việc quăng vô [tool](https://www.dcode.fr/monoalphabetic-substitution) này là xong =))

Một đặc điểm chung của 3 bài là cuối mỗi `message` đều có dạng `The flag is picoCTF{...}`. Từ những manh mối đó và khả năng suy đoán từ tiếng Anh sẽ giúp ta dễ dàng vượt qua 3 thử thách này =))
## Flag
**sub0:   `picoCTF{5UB5717U710N_3V0LU710N_357BF9FF}`**
**sub1:   `picoCTF{FR3QU3NCY_4774CK5_4R3_C001_6E0659FB}`**
**sub2:   `picoCTF{N6R4M_4N41Y515_15_73D10U5_42EA1770}`**

