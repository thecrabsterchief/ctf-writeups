from Crypto.PublicKey import RSA
from Crypto.Util.number import *
from Crypto.Cipher import AES
from pwn import *

def sign():
    io.sendlineafter(b">> ", b"1")
    m, s = eval(io.recvline().decode().strip())
    return m, s

def enc_flag():
    io.sendlineafter(b">> ", b"2")
    io.recvuntil(b"encrypted_key=")
    rsa_ct = int(io.recvline())
    aes_ct, iv = eval(io.recvline().decode().strip())

    return rsa_ct, (aes_ct, iv)

def get_pub():
    io.sendlineafter(b">> ", b"3")
    return io.recvuntil(b"-----END PUBLIC KEY-----\n").decode()

if __name__ == "__main__":
    io = remote("34.154.18.2", 6954)

    rsa_key = RSA.importKey(get_pub())
    
    N = rsa_key.n
    e = rsa_key.e

    m, s = sign()
    p = GCD(pow(s, e, N) - m, N)
    q = N//p
    d = inverse(e, (p - 1)*(q - 1))

    c, (ct, iv) = enc_flag()
    key = pow(c, d, N)

    cipher = AES.new(long_to_bytes(key), AES.MODE_CBC, bytes.fromhex(iv))
    flag = cipher.decrypt(bytes.fromhex(ct))
    print(flag)