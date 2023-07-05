# NSA Backdoor

## Challenge

Đây là bài cuối cùng và cũng là bài mình thích nhất vì nó sử dụng một số kiến thức số học khá thú vị =)). 

Đầu tiên quan sát `p - 1` và `q - 1` đều là `smooth number` như bài `Very Smooth` nên ta dễ dàng `factor` được `N` từ đó `factor` được `phi(N)`

```py
factorial = 1
for i in range(1, 100000):
    factorial *= i
 
p = gcd(pow(2, factorial, n) - 1, n)
q = n//p

p_phi_factor, q_phi_factor = [], []
for i in range(2, 200000):
    if (p - 1)%i == 0:
        p_phi_factor.append(i)
    if (q - 1)%i == 0:
        q_phi_factor.append(i)

# n_phi_factor = [4, 20611, 30971, 32987, 33107, 33151, 33289, 33457, 33679, 34123, 34897, 35023, 35227, 35671, 36151, 37049, 37139, 39313, 39541, 40087, 40237, 40787, 41257, 41333, 41351, 41999, 42083, 42239, 43177, 43627, 44617, 44789, 45179, 46381, 46619, 46861, 47111, 48883, 49157, 50359, 50527, 50773, 50777, 50857, 50951, 51307, 51361, 51383, 51593, 52889, 52967, 53047, 54037, 54673, 56479, 56569, 57301, 58963, 59651, 61027, 61441, 61507, 62347, 62929, 62969, 63587, 64171, 64621, 65497, 66343, 67559, 67651, 67759, 67801, 68239, 71633, 73421, 74159, 74821, 77347, 78977, 79813, 82129, 82301, 82787, 84047, 87181, 87959, 88117, 88241, 89137, 89203, 90583, 91873, 92623, 93557, 93601, 94253, 94649, 95369, 97813, 97849, 98017, 99431, 100459, 101377, 101929, 103217, 103549, 106591, 106979, 111697, 112061, 112253, 112397, 114013, 116107, 116881, 117617, 118739, 119159, 119503, 120847, 121843, 121909, 124471, 126127, 126241, 130729]
# p = 99755582215898641407852705728849845011216465185285211890507480631690828127706976150193361900607547572612649004926900810814622928574610545242732025536653312012118816651110903126840980322976744546241025457578454651121668690556783678825279039346489911822502647155696586387159134782652895389723477462451243655239
# q = 145188107204395996941237224511021728827449781357154531339825069878361330960402058326626961666006203200118414609080899168979077514608109257635499315648089844975963420428126473405468291778331429276352521506412236447510500004803301358005971579603665229996826267172950505836678077264366200199161972745420872759627
```

Tới đây ta gặp phải bài toán [discrete logarithm](https://en.wikipedia.org/wiki/Discrete_logarithm): tức tìm `x` sao cho `g^x = h (mod n)` với `g, h, n` cho trước. Nhưng với `n` lớn thì chúng ta cần xử lí một chút, ý tưởng chính như sau:

* Gọi `q` là ước của `phi(n)`: từ `g^x = h (mod n) => (g^(phi(n)/q))^x = h^(phi(n)/q) (mod n)`
* Đặt `G = pow(g, phi(n)/q, n), H = pow(h, phi(n)/q, n) => G^x = H (mod n)`. Tới đây chú ý `pow(G, q, n) = pow(G, phi(n), n) = 1 => ord_G(n) | q`
* Tới đây lại để ý vì `q - 1` và `p - 1` đều `smooth` nên `q | phi(N)` thì `q` sẽ nhỏ (tầm `16 - 17 bits`) do đó ta chuyển về bài toán `DLP` nhỏ hơn trên `subgroup` của `n`: tìm `x_q` thuộc `[1, q]` sao cho `pow(G, x_q, n) == H` (`q` nhỏ nên hoàn toàn `brute-force` được, nhưng ở đây để nhanh hơn mình dùng [Shank's](https://en.wikipedia.org/wiki/Baby-step_giant-step)). Khi đó nếu `pow(g, x, n) == h => x = x_q (mod q)`
* Khi ta có được `x = x_q (mod q)` với `q` duyệt qua hết tập ước của `phi(n)` thì ta hoàn toàn giải được bài toán `DLP` ban đầu bằng cách dùng [CRT](https://en.wikipedia.org/wiki/Chinese_remainder_theorem)

**Chú ý:** Đây cũng là ý tưởng chính của thuật toán [Pohlig-Hellman](https://en.wikipedia.org/wiki/Pohlig%E2%80%93Hellman_algorithm)

```py
def Shank_DLP(g, h, mod, ord):
    n =  1 + iroot(ord, 2)[0]
    base, BASE = g, pow(g, -n, mod)

    b_step = {pow(base, i, mod) : i for i in range(1, n+1)}
    g_step = {h * pow(BASE, i, mod) % mod : i for i in range(1, n+1)}

    for b in b_step:
        if b in g_step:
            return (b_step[b] + g_step[b] * n) % ord

def Pohlig_DLP(c, g, n_phi, n, n_factor):
    lst = []
    for x in n_factor:
        C, G = pow(c, n_phi//x, n), pow(g, n_phi//x, n)
        lst.append(Shank_DLP(G, C, n, x))
    return lst

def crt(a, m):
    M, D, n = 1, 0, len(m)
    for x in m:
        M, D = M*x, gcd(D, x)
    if D != 1:
        return -1
    b = [M//x for x in m]
    c = [inverse(b[i], m[i]) for i in range(n)]
    x = 0
    for i in range(n):
        x = (x + a[i]*b[i]*c[i])%M
    return x

rm_n = Pohlig_DLP(c, g, (p - 1) * (q - 1), n, n_phi_factor)


flag = crt(rm_n, n_phi_factor)

print(long_to_bytes(flag))
```

Oopss! Có gì đó không ổn... Ban đầu mình cũng khá bối rối vì check đi check lại thì `flag` vẫn thỏa `pow(g, flag, n) == c`
Ngẫm lại thì `flag` mình vừa tính được rất lớn (vì tính `CRT` sẽ ra kết quả theo `mod phi(n)` và nghiệm tổng quát sẽ là `x = flag (mod phi(n))`) trên thực tế nghiệm trên chưa quét hết toàn bộ tập nghiệm (vì toàn bộ nghiệm `x` sẽ là `x = flag (mod ord_g(n))`) Vậy mình sẽ cần thêm công đoạn tính `ord_g(n)`, nhưng thực tế chì cần tìm ra bội của `ord_g(n)` (tất nhiên phải nhỏ hơn `phi(n)`) vì mình đang mong muốn làm `flag` nhỏ lại...
```py
def order(g, n, n_phi_Euler_factor, n_phi_Euler):
    for q in n_phi_Euler_factor[::-1]:
        Ord = n_phi_Euler//q
        if pow(g, Ord, n) == 1:
            return Ord
    return n_phi_Euler

ord_g = order(g, n, n_phi_factor, (p - 1) * (q - 1))
flag = crt(rm_n, n_phi_factor)

print(long_to_bytes(flag))
```
Và lần này đã thành công !!!

## FLag
**`picoCTF{e032a664}`**