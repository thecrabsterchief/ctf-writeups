from base64 import *

cmplx = "78 6 1 65 0 57 1 78 0 28 1 99 0 23 1 78 0 9 1 2 1 33 1 78 0 6 1 81 0 39 1 78 0 9 1 2 1 50 0 40 1 16 1 82 0 25 1 77 0 45 1 103 0 49 0 41 1 16 1 77 0 42 1 78 0 6 1 23 1 15 1 79 0 5 1 77 0 50 0 28 1 28 1 1 1 15 1 79 0 68 0 31 1 53 0 25 1 9 1 2 1 49 0 29 1 44 1 77 0 50 0 27 1 45 1 107 0 50 0 29 1 5 1 77 0 52 0 52"
cmplx = [int(char) for char in cmplx.split()]

def rev_somestuff(cmplx):
    # reverse list `data`
    data = [cmplx[0]]
    
    for i in range(1, len(cmplx)- 1, 2):
        dt = cmplx[i + 1] * data[-1] + cmplx[i]
        data.append(dt)
    
    # reverse message
    b64enc = ''.join(chr(num) for num in data) 
    return bytes.fromhex(b64decode(b64enc).decode()).decode()

def re_hide(enc, secret):
    msg = ""
    for i in range(len(enc)):
        char = enc[i]
        if (char.isupper()):
            msg += chr((ord(char) - pow(-1,i)*secret - 65) % 26 + 65)
        elif (char.islower()):
            msg += chr((ord(char) - pow(-1,i)*secret - 97) % 26 + 97)
        elif (char.isdecimal()):
            msg += chr((ord(char) - pow(-1,i)*secret - 48) % 10 + 48)
        else:
            msg += char
    return msg

print(re_hide(rev_somestuff(cmplx), 5))

# Flag: WhiteHate{K1n_0F_tH3_5T41n3d_B14d3}