import requests

x = int('ce205d44c14517ba33f3ef313e404537854d494e28fcf71615e5f51c9a459f42', 16)
y = int('6080e22d9a44a5ce38741f8994ac3a14a6760f06dd1510b89b6907dfd5932868', 16)


io = requests.post(url="http://127.0.0.1:1984/verify_signature", json={
    "message_hash": "00",
    "signature": (int.to_bytes(x, byteorder='big', length=32) * 2).hex()
})

print(io.text)