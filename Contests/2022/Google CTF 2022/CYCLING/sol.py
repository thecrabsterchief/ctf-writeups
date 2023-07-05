from Crypto.Util.number import *
from factordb.factordb import FactorDB

e = 65537
n = 0x99efa9177387907eb3f74dc09a4d7a93abf6ceb7ee102c689ecd0998975cede29f3ca951feb5adfb9282879cc666e22dcafc07d7f89d762b9ad5532042c79060cdb022703d790421a7f6a76a50cceb635ad1b5d78510adf8c6ff9645a1b179e965358e10fe3dd5f82744773360270b6fa62d972d196a810e152f1285e0b8b26f5d54991d0539a13e655d752bd71963f822affc7a03e946cea2c4ef65bf94706f20b79d672e64e8faac45172c4130bfeca9bef71ed8c0c9e2aa0a1d6d47239960f90ef25b337255bac9c452cb019a44115b0437726a9adef10a028f1e1263c97c14a1d7cd58a8994832e764ffbfcc05ec8ed3269bb0569278eea0550548b552b1
ct = 0x339be515121dab503106cd190897382149e032a76a1ca0eec74f2c8c74560b00dffc0ad65ee4df4f47b2c9810d93e8579517692268c821c6724946438a9744a2a95510d529f0e0195a2660abd057d3f6a59df3a1c9a116f76d53900e2a715dfe5525228e832c02fd07b8dac0d488cca269e0dbb74047cf7a5e64a06a443f7d580ee28c5d41d5ede3604825eba31985e96575df2bcc2fefd0c77f2033c04008be9746a0935338434c16d5a68d1338eabdcf0170ac19a27ec832bf0a353934570abd48b1fe31bc9a4bb99428d1fbab726b284aec27522efb9527ddce1106ba6a480c65f9332c5b2a3c727a2cca6d6951b09c7c28ed0474fdc6a945076524877680
k = 2**1025 - 3

# Thử factor số k + 1 xem thử tập ước nó ntn ~~
f = FactorDB(k + 1)
f.connect()
fac = f.get_factor_list()
assert len(fac) == 17

# sinh số t từ tập ước của k + 1 như mình đã trình bày ở trên
t = 1
for i in range(1 << 17):
    d = 1
    masks = i
    for j in range(17):
        if masks & 1:
            d *= fac[j]
        masks >>= 1
    
    if isPrime(d + 1):
        t *= d + 1
print(t)
d = inverse(e, t)
flag = long_to_bytes(pow(ct, d, n))
print(f'[+] Flag: {flag.decode()}')

# [+] Flag: CTF{Recycling_Is_Great}
