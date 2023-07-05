from PIL import Image
from randcrack import RandCrack

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

if __name__ == '__main__':
    flag_first_line = Image.open("./part.png")
    flag_first_line_px = flag_first_line.load()
    lenX, lenY = flag_first_line.size

    flag_enc = Image.open("./out.png")
    flag_enc_px = flag_enc.load()

    flag = Image.new("RGBA", (lenX, lenY), "white")
    flag_px = flag.load()

    for y in range(lenY):
        if y == 0:
            res = []
            for x in range(lenX):
                # copy first line
                flag_px[x, y] = flag_first_line_px[x, y]

                # collect random key
                r, g, b, a = flag_first_line_px[x, y]
                r_out, g_out, b_out, a_out = flag_enc_px[x, y]
                r_key, g_key, b_key, a_key = xor_tuple((r_out, g_out, b_out, a_out), (r, g, b, a))

                res.append(rgba2int((r_key, g_key, b_key, a_key)))
            
            # need at least 624 numbers to crack random
            assert len(res) >= 624
            rc = RandCrack()
            for num in res[:624]: rc.submit(num)
            for _ in range(624, lenX): rc.predict_getrandbits(32)

        else:
            for x in range(lenX):
                rand = rc.predict_getrandbits(32)
                rr, rg, rb, ra = int2rgba(rand)
                r_out, g_out, b_out, a_out = flag_enc_px[x, y]
                flag_pix = xor_tuple((rr, rg, rb, ra), (r_out, g_out, b_out, a_out))

                flag_px[x, y] = flag_pix
    
    flag.save("FLAG.png")