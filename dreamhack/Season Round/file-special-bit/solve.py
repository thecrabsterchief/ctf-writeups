from pwn import *

poc = ssh(host="host3.dreamhack.games", user="chall", port=15250, password="dhbeginnerchall1")

io = poc.process(["./chall", "flag"])

io.sendlineafter(b": \n", b"1000")
io.sendlineafter(b": \n", b"2123")
io.interactive()
