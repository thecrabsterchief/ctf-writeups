#!/usr/bin/python3
from xiao import flag

def check(flag):
	for i in flag:
		assert len(format(ord(i), 'b')) == 7

def zero_to_one(bin_):
	str_ = ''
	for i in bin_:
		if i == '0': str_ +='1'
		else: str_ += '0'
	else: print('End.')
	return str_

def convert(flag):
	bin_ = ' '.join(format(ord(x), 'b') for x in flag).replace(' ','1')
	return print("bin_: ",zero_to_one(bin_))

if __name__ == '__main__':
	check(flag)
	convert(flag)
#bin_:  01010000001011100010110000010110001101000110111000111100000101100000100000101100001001000001111000100000000110100001011001000000010000000011101000010100000101100100000000101100010000000011011000100000001000100001011001000000001110000011110000011010001101000000010