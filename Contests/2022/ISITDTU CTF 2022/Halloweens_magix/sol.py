from sage.all import *
from Crypto.Util.number import bytes_to_long

def bytes2matrix(b):
	return matrix(ZZ, 4, 4, [bytes_to_long(b[i:i + 2]) for i in range(0, len(b), 2)])

png_header = matrix(ZZ, [
	[137,  80,  78,  71],
	[ 13,  10,  26,  10],
	[  0,   0,   0,  13],
	[ 73,  72,  68,  82]
])

if __name__ == '__main__':
	encrypted_flag = open("./Halloweens_magix/flag.png.enc", "rb").read()
	blocks = [bytes2matrix(encrypted_flag[i:i + 32]) for i in range(0, len(encrypted_flag), 32)]

	key = ~png_header * blocks[0]
	
	flag = b''
	for block in blocks:
		flag += bytes((block * key.inverse()).list())

	with open('./Halloweens_magix/flag.png', 'wb') as f:
		f.write(flag)




