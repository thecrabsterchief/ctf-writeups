import gmpy2
import random


def legendary(a, n):
    assert n > a > 0 and n % 2 == 1
    t = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            r = n % 8
            if r == 3 or r == 5:
                t = -t
        a, n = n, a
        if a % 4 == n % 4 == 3:
            t = -t
        a %= n
    if n == 1:
        return t
    else:
        return 0


class PseudoRandomNumberGenerator:
    def __init__(self, key, prime=0xFFFFFFFFFFC5):
        assert gmpy2.is_prime(prime) and 0 <= key < prime

        self.x = 0
        self.key = key
        self.prime = prime

    def __iter__(self):
        return self

    def __next__(self):
        if self.x >= self.prime:
            raise StopIteration

        result = (legendary(self.x + self.key, self.prime) + 1) // 2
        self.x += 1
        return result


if __name__ == '__main__':
    secret = random.getrandbits(48)
    prng = PseudoRandomNumberGenerator(secret)

    for _ in range((1 << 24) // 4):
        hexdigit = (next(prng) << 3) + (next(prng) << 2) \
                 + (next(prng) << 1) + next(prng)
        print(f'{hexdigit:01X}', end='')

    print()
    print(f'GoN{{{secret:012X}}}')
