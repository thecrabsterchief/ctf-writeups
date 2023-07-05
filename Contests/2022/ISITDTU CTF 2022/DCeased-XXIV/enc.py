from PIL import Image
import random, time

def xor(a):
	return a[0] ^ a[1]

def xor_tuple(a, b):
	return tuple(i for i in map(xor, zip(*[a, b])))

def rgba2int(rgba: tuple):
	ret = 0
	for i in range(3, -1, -1):
		ret += rgba[i] << 8*(3 - i)
	return ret

def int2rgba(n):
	r, g, b, a = tuple([(n >> 8*i) & 0xff for i in range(3, -1, -1)])
	return (r, g, b, a)

img = Image.open('flag.png')

random.seed(time.time())

px = img.load()
x_len, y_len = img.size

new = Image.new('RGBA', (x_len, y_len), 'white')
px1 = new.load()

for y in range(y_len):
	for x in range(x_len):
		rand = random.getrandbits(32)
		rr, rg, rb, ra = int2rgba(rand)
		r, g, b, a = px[x, y]
		new_pix = xor_tuple((rr, rg, rb, ra), (r, g, b, a))
		px1[x, y] = new_pix

new.save('out.png')

