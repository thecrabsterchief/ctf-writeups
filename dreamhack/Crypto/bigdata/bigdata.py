from Crypto.Util.number import *
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import os

datas = []
data_num = 1000000

for _ in range(data_num):
	datas.append(bytes_to_long(os.urandom(16)))

key = 0
for data in datas:
	key = key^data

flag = open("flag.txt", "r").read()

cipher = AES.new(key.to_bytes(16, "big"), AES.MODE_ECB)
enc_flag = cipher.encrypt(pad(flag.encode(), 16))

print(f"enc_flag = {bytes.hex(enc_flag)}")

while 1:
	try:
		idx = int(input("> "))
		assert idx < data_num and idx >= 0
		print(datas[idx])
	except:
		exit()
