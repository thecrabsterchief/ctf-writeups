from string import *

User = open('usernames.txt', 'r').read().split('\n')
Pass = open('passwords.txt', 'r').read().split('\n')

Accounts = {u:p for (u, p) in zip(User, Pass)}

ciphertext = Accounts['cultiris']
key = (ord(ciphertext[0]) - ord('p')) % 26

flag = ""
low = ascii_lowercase
up = ascii_uppercase

for char in ciphertext:
    if char in low:
        flag += low[(low.index(char) - key) % 26]
    elif char in up:
        flag += up[(up.index(char) - key) % 26]
    else:
        flag += char 

print(flag)

# Flag: picoCTF{C7r1F_54V35_71M3}