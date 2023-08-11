from base64 import *

import sys
sys.path.insert(1, "/home/viensea1106/Projects/hash-length-extension")

import HashTools

hashing_input  = b64decode("dXNlcm5hbWU9Z3Vlc3QmaXNMb2dnZWRJbj1GYWxzZQ==")
crypto_segment = b64decode("ZGZmNTlmZWI4YWNhYjgyMDk5ZjZlNTlkZTM1YmY1ODRjNzJjMGZmZjM2Mjk4YzlkMzY3MTVjYmRlNWUxODkwMGYxZDdkNGE5MGJjNjMyZWFlOWU3MjZhOTMxMjYwNzUxZjZhNzdiMzc1Mjc0ZmQ1ZGYxYjc3NmVhMDc3MDI1MzA=").decode()

magic = HashTools.new(algorithm="sha512")
new_data, new_sig = magic.extension(
    secret_length=16, original_data=hashing_input,
    append_data=b"&isLoggedIn=True", signature=crypto_segment
)

cookie = "{}.{}".format(b64encode(new_data).decode(), b64encode(new_sig.encode()).decode())

print(cookie)