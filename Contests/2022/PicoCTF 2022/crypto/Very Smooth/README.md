# Very Smooth

## Challenge

Đầu tiên ta ngó qua file **gen.py**. Hmm... nhìn qua thì đây là một bài **RSA**, mấu chốt để giải là tìm cách **factor modulos n** ta sẽ dựa vào hàm **get_prime** để khai thác. Tên bài gợi cho ta khái niệm về [smooth number](https://en.wikipedia.org/wiki/Smooth_number#:~:text=In%20number%20theory%2C%20an%20n,13%20are%20not%207%2Dsmooth.)

Ta thấy: **p - 1** là **16-smooth** và **q - 1** là **17-smooth** (tức các ước nguyên tố của **p - 1** đều nhỏ hơn **16 bits** tương tự với **q - 1** là **17 bits**). Vậy ý tưởng để **factor n** như sau:

* Chọn **m** sao cho **2^m = 1 (mod p)** và **2^m != 1(mod q)**. Khi đó **p = gcd(2^m - 1, N)**
* Do **p - 1** là **16-smooth** nên số **k!** với **k** đủ lớn (tối đa **16 bits**) sẽ chia hết cho **p - 1**, nhưng vì **q - 1** là **17-smooth** nên **k!** sẽ không chia hết cho **q - 1**
* Khi đó theo [Fermat](https://en.wikipedia.org/wiki/Fermat%27s_little_theorem) thì **2^k! = 1 (mod p)** và **2^k! = 2^r (mod q)** với **r = k! (mod q - 1)** xác xuất để **2^r = 1 (mod q)** sẽ thấp, do đó ta hoàn toàn có thể tìm được số **m** thỏa mãn và **factor** được **N**

**Chú ý:** Thuật toán ở trên là [Pollard's p − 1 algorithm](https://en.wikipedia.org/wiki/Pollard%27s_p_%E2%88%92_1_algorithm)

## Solution
**py
n = 0x6c5f4a08d820579e606aeb3800d1602c53825167d01bd7c87f43041afdc82877c50bbcc7830a0bf8c718fc9016e4a9e73ff0dfe1edd38688acb6add89b2bd6264d61e2ce0c9b3b0813b46b0eb1fcfc56b9f7f072ba2e1e986e6420f8ad9063e10fa9bca464b23fcf0135f95dc11a89bfddf2e81572c196f4362ea551aee18b343638d9d703b234e788bff4ddc3e885da77c7940a0fa670ddc1604646871f0739199fa7fa01f9ed7d84fb9f0cc82965450e7c97153fec84ef8e10a7fceb37a90e847a012528c733070e9ab751215b13a7e2d485089c0c4d00b81dbab382ef7681c717c76c2b14ce6495ef121540653561c3dd519c5f6e2ead18e9d90f3769a029
c = 0x42cbc15285a307d86ac5184c89d6bea5ebdc0a7546debedfe40af69fa6813eaf11ef86543349062587621b845e82817cf7f154c067733ee8b23a75e45861ee0c45a07e702dcb199adffa4ca0892fcd85abfe9e9b59c2ac2df7811a656a3fda16f385972107481409e33e820a19864233b8a35bc49734dc337786dc06c0460a4ec9fc06d16fd66a43654390a526ab0a6239b14427a9868399f6e4863ac04539690357e9a4fa67450286febd9a97dd07864f516f6756c2ffad0b1ba5882980f0089605f0def91120a80a448f77ec272be41de0e11695ba7d0c8899b1d9e8905a1b5e95a755e584dead086f35844052f261e8dcd0d6cffdce38cd5181235dfa0745
e = 0x10001

from Crypto.Util.number import long_to_bytes
from gmpy2 import gcd

factorial = 1
for i in range(1, 1 << 16):
    factorial *= i
 
p = gcd(pow(2, factorial, n) - 1, n)
q = n//p

n_phi_Euler = (p - 1) * (q - 1)
d = pow(e, -1, n_phi_Euler)
flag = long_to_bytes(pow(c, d, n))

print(flag)
**

## Flag
****picoCTF{148cbc0f}****