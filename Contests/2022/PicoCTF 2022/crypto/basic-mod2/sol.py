from string import *
letter = ascii_uppercase + digits + '_'

ciphertext = "104 290 356 313 262 337 354 229 146 297 118 373 221 359 338 321 288 79 214 277 131 190 377"
ciphertext = [int(num) for num in ciphertext.split(" ")]

flag = ''.join(letter[pow(num, -1, 41) - 1] for num in ciphertext)

print('picoCTF{' + flag + '}')

# Flag: picoCTF{1nv3r53ly_h4rd_8a05d939}