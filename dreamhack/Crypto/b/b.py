from Crypto.Util.number import getPrime, bytes_to_long
try:
	b = int(input())
	m = int.from_bytes(open("flag.txt", "rb").read(), "big")
	if b * 2 < m.bit_length(): input("I'm not really sure about this");exit()
	for _ in range(b):
		n = getPrime(b) * getPrime(b)
		c = pow(m, 65537, n)
		print(f"Data {_ + 1}: {c = }, {n = }")
except: pass