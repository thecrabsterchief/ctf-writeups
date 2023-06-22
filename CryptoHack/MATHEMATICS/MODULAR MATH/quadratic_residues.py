p = 29
ints = [14, 6, 11]

for n in ints:
    if pow(n, (p - 1)//2, p) == 1:
        for a in range(p):
            if pow(a, 2, p) == n:
                print(a)
                exit()

# Flag: 8