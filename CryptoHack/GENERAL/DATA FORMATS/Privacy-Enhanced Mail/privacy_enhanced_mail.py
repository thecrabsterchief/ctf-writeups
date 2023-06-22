from Crypto.PublicKey import RSA

key = RSA.importKey(open("./privacy_enhanced_mail.pem", "r").read())
print(key.d)