from pwn import *
from jvdsn.attacks.knapsack.low_density import attack

def solve_knapsack(weights, profits, max_weight):
    # https://www.geeksforgeeks.org/printing-items-01-knapsack/
    assert len(weights) == len(profits)
    n  = len(weights)
    dp = [
        [0 for i in range(max_weight + 1)] for j in range(n + 1)
    ]

    for i in range(n + 1):
        for w in range(max_weight + 1):
            if i == 0 or w == 0:
                dp[i][w] = 0

            elif weights[i - 1] <= w:
                dp[i][w] = max(
                    profits[i - 1] +  dp[i - 1][w - weights[i - 1]], 
                    dp[i - 1][w]
                )
            else:
                dp[i][w] = dp[i - 1][w]
    
    max_profit = dp[n][max_weight]
    items = []
    for i in range(n, 0, -1):
        if max_profit <= 0:
            break
        if max_profit != dp[i - 1][max_weight]:
            items.append(i - 1)
            
            max_weight -= weights[i - 1]
            max_profit -= profits[i - 1]
    return items

io = process(["python3", "challenge.py"])
io.recvline()

# Part 1: Knapsack
for i in range(10):
    weights = eval(io.recvline().decode().strip())
    profits = eval(io.recvline().decode().strip())

    io.recvuntil(b"Knapsack Capacity: ")
    max_weight = int(io.recvline())

    items = solve_knapsack(weights, profits, max_weight)
    io.sendlineafter(b": ", " ".join(str(x) for x in items).encode())
    io.recvline()

flag1 = eval(io.recvline().strip().decode())

# Part 2: Backpack
for i in range(10):
    B = eval(io.recvline().decode().strip())
    
    io.recvuntil(b": ")
    S = int(io.recvline())
    secret = int("".join(
        str(x) for x in attack(B, S)
    ), 2)
    io.sendlineafter(b": ", str(secret).encode())
    io.recvline()

flag2 = eval(io.recvline().strip().decode())
io.close()

flag = flag1 + flag2
print("[+] Flag:", flag.decode())