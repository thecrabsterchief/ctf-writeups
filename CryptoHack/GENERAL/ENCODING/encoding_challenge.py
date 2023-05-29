from tqdm import tqdm
from pwn import *
from Crypto.Util.number import long_to_bytes
from base64 import b64decode
import json
from string import ascii_lowercase
from codecs import decode

class challenge:
    def __init__(self, HOST, PORT) -> None:
        self.io = remote(HOST, PORT)
    
    def solve(self):
        chall = json.loads(self.io.recvline().strip().decode())
        
        if chall['type'] == 'base64':
            answer = {'decoded': b64decode(chall['encoded']).decode()}
            self.io.sendline(json.dumps(answer).encode())
        
        elif chall['type'] == 'bigint':
            answer = {'decoded': long_to_bytes(int(chall['encoded'], 16)).decode()}
            self.io.sendline(json.dumps(answer).encode())
        
        elif chall['type'] == 'hex':
            answer = {'decoded': bytes.fromhex(chall['encoded']).decode()}
            self.io.sendline(json.dumps(answer).encode())
        
        elif chall['type'] == 'utf-8':
            answer = {'decoded': bytes(chall['encoded']).decode()}
            self.io.sendline(json.dumps(answer).encode())
        
        else:
            answer = {'decoded': decode(chall['encoded'], 'rot_13')}
            self.io.sendline(json.dumps(answer).encode())

    def interactive(self):
        return self.io.interactive()
    
if __name__ == '__main__':
    HOST = "socket.cryptohack.org"
    PORT = 13377
    chall = challenge(HOST, PORT)
    
    for i in tqdm(range(100)):
        chall.solve()
    
    chall.interactive()