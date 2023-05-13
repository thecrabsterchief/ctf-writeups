from pwn import *

# ssh picoplayer@saturn.picoctf.net -p 56610
s = ssh(host="saturn.picoctf.net", port=56610, user="picoplayer", password="password")

sh = s.shell()
sh.interactive()