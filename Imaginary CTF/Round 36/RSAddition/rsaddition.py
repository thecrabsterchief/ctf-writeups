from Crypto.Util.number import *

flag = b"ictf{REDACTED}"


e = 65537
p, q = getPrime(512), getPrime(512)
n = p * q

# there are only ~2**512 distinct integer pairs that add up to this value
# should be fine to show to the user, takes too long to brute force
summed = p+q

ct = pow(bytes_to_long(flag), e, n)

print(f"ct={ct}\ne={e}\nn={n}\nsummed={summed}")
