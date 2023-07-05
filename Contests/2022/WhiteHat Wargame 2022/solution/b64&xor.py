from base64 import b64decode

def xor(a, b):
    return bytes([x^y for (x, y) in zip(a, b)])

encoded = "NFwcKxN4DxMGLVxFABUAADgQFgAqMgNRMQ89PAAbNyldXg4iF1xBJik="

b64enc = b64decode(encoded)
known = b'WhiteHat{'

key = xor(known, b64enc)

KEY = b''
for i in range(len(b64enc)):
    KEY += bytes([key[i % len(key)]])

flag = xor(KEY, b64enc) + key

print(flag)

# Flag: WhiteHat{Nh0_c0n_mu4_mua_h@_4nh_m0i_th4y_c4u_v0ng}