#!/usr/bin/env python3

from random import randint

def seesawr(s, key):
    return bytes((c + (1-2*i)*key)%256 for i, c in enumerate(s))

flag = open("flag.txt", 'rb').read()

key = randint(0, 2**128)
print(seesawr(flag, key))

# Output:
# b'\xc3\tf\xa4\x058\x83\xd1%e\xc6\rI\x97\xe1;\x8f\xc9\x1a]\xb7\x05T\x93\xd9)s\xc3\x1dW\xb4\xbbF\x8f\xdd#i\xb9\x03S\xad\xe7D}\xcd\x1ec\xba\x06c'