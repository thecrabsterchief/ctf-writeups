from string import *
letter = ascii_uppercase + digits + '_'

ciphertext = "91 322 57 124 40 406 272 147 239 285 353 272 77 110 296 262 299 323 255 337 150 102"
ciphertext = [int(num) for num in ciphertext.split(" ")]

flag = ''.join(letter[num % 37] for num in ciphertext)

print('picoCTF{' + flag + '}')

# Flag: picoCTF{R0UND_N_R0UND_ADD17EC2}

