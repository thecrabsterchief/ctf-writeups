import base64

def hide(flag,secret):
    result = ""
    for i in range(len(flag)):
        char = flag[i]
        if (char.isupper()):
            result += chr((ord(char) + pow(-1,i)*secret - 65) % 26 + 65)
        elif (char.islower()):
            result += chr((ord(char) + pow(-1,i)*secret - 97) % 26 + 97)
        elif (char.isdecimal()):
            result += chr((ord(char) + pow(-1,i)*secret - 48) % 10 + 48)
        else:
            result += char
    return result
def somestuff(message):
    result = ""
    text = message.encode().hex()
    newtext = base64.b64encode(text.encode('ascii')).decode('ascii')
    for i in range(len(newtext) - 1):
        result += str(ord(newtext[i])) + ' '
    result += str(ord(newtext[len(newtext) - 1]))
    data = result.split()
    cmplx = []
    cmplx.append(data[0])
    for i in range(len(data)-1):
        cmplx.append(str(int(data[i+1])%int(data[i])))
        cmplx.append(str(int(data[i+1])//int(data[i])))
    cmplx.append(data[len(data)-1])
    return cmplx
def modify(mylist):
    mystr = ' '.join(mylist)    
    return mystr 
if __name__ == '__main__':
    print(modify(somestuff(hide("K1",5))))


# Number sequence: 
# 78 6 1 65 0 57 1 78 0 28 1 99 0 23 1 78 0 9 1 2 1 33 1 78 0 6 1 81 0 39 1 78 0 9 1 2 1 50 0 40 1 16 1 82 0 25 1 77 0 45 1 103 0 49 0 41 1 16 1 77 0 42 1 78 0 6 1 23 1 15 1 79 0 5 1 77 0 50 0 28 1 28 1 1 1 15 1 79 0 68 0 31 1 53 0 25 1 9 1 2 1 49 0 29 1 44 1 77 0 50 0 27 1 45 1 107 0 50 0 29 1 5 1 77 0 52 0 52
# Secret number:
# 5