# glitch in the matrix

## Solution

Một bài khá hay, sử dụng một chút kiến thức về Linear Algebra... Đầu tiên ta thử phân tích source code:

* Đề import 1 ma trận `SECRET_BASIS` 128x128
* Hàm `f(M, C)` là phép nhân ma trận `C(1xm)` với ma trận `M(mxn)`, hay bản chất là lấy tổ hợp tuyến tính các hàng của ma trận `M`
* Hàm `encrypt(msg)` thực hiện như sau, đầu tiên chuyển `msg` về dạng binary, và chia `SECRET_BASIS` làm đôi (64x128) tạm gọi là `A` và `B`. Lúc này với mỗi bit của `msg`: nếu là bit 1 thì lấy tổ hợp tuyến tính ngẫu nhiên các hàng của basis `A`, còn nếu là bit 0 thì lấy tổ hợp tuyến tính ngẫu nhiên các hàng của basis `B`. Ciphertext là tổng hợp các kết quả vừa tìm được
* Để lấy được flag ta phải đoán chính xác một cái `token` 8 bytes được sinh ngẫu nhiên từ đề thêm vào đó ta cũng được phép encrypt cái token này

Để ý rằng tại vị trí cùng là bit 1 (hoặc bit 0) thì là tổ hợp tuyến tính của basis A (hoặc basis B). Nhắc lại một chút kiến thức về đại số tuyến tính: tập hợp tổ hợp tuyến tính các hàng của một ma trận M là một không gian vector có dim <= rank(M).

Như vậy mình mới đi tới ý tưởng như sau: đầu tiên yêu cầu server encrypt secret_token 128 lần. Tại mỗi vị trí output tương ứng với từng bit của secret_token mình sẽ nhóm lại với nhau, tạo thành một ma trận 128x128. 

Như vậy mỗi ma trận output này đặc trưng cho từng bit của secret_token và chúng là tập con của không gian vector sinh bởi A hoặc B. Do đó rank của mỗi ma trận đều <= rank(A) (hoặc rank(B)) và trên thực tế mình tính thì tất cả đều bằng 64 (và vì ma trận A và B đều là 64x128 nên chứng tỏ rằng cả hai đều ma trận cơ sở!)

Vậy nếu ta cố định ma trận đầu tiên (S), lấy tất cả ma trận còn lại (M) cộng với ma trận đầu tiên. 
* Nếu rank(M + S) = 64 => M và S được sinh cùng basis => cùng tính chất bit
* Nếu rank(M + S) > 64 => M và S được sinh khác basis => khác tính chất bit
Ta giả sử bit đầu là "0" => hoàn toàn tìm được các bit còn lại => done!

Code mình để [ở đây](./sol.py)

**Flag: ISITDTU{c8ac07f0e7d322179d5e6cfe78e5f70fc4ddc78d}**