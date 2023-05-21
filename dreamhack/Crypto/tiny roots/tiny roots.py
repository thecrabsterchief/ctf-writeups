from Crypto.Util.number import *

FLAG = open('../../flag.txt','rb').read()
FLAG = bytes_to_long(FLAG)

p = getPrime(1024)
q = getPrime(1024)
assert p > q

n = p * q
e = getPrime(128)

beta = 0.4
epsilon = beta ** 2 / 7

upper_bound = p.bit_length()
lower_bound = int(n.bit_length() * (beta ** 2 - epsilon))

MSB = p & (pow(2,upper_bound) - pow(2,lower_bound))

# encryption
ciphertext = pow(FLAG,e,n)

print(f'Here is the flag : {ciphertext}\n')
print(f'I don\'t know the secret key... except some bits of p...\n{MSB}\n')
print(f'But I know the public key !! Can You make it??\n({n},{e})')
