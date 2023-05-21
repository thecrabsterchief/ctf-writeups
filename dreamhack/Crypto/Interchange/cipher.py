from Crypto.Cipher import AES
from Crypto.Util import Counter

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * bytes([BS - len(s) % BS])
unpad = lambda s : s[0:-s[-1]]

class cipher:
    def __init__(self, key): 
        self.key = key 
        self.iv = None
        self.update_iv() 
        self.str = None  

    def update_iv(self):
        if not self.iv:
            self.iv = self.key
        self.iv = AES.new(self.iv, AES.MODE_ECB).encrypt(self.key)
        self.iv = AES.new(self.key, AES.MODE_ECB).decrypt(self.iv)
    
    def __repr__(self):
        return self.str

class CBC_cipher(cipher): 
    def __init__(self, key): 
        super().__init__(key)
        self.str = "CBC"
     
    def encrypt(self, pt): 
        pt = pad(pt.encode()) 
        ct = AES.new(self.key, AES.MODE_CBC, self.iv).encrypt(pt)
        res = self.iv + ct
        self.update_iv()
        return res
     
    def decrypt(self, e): 
        iv = e[:BS] 
        return unpad(AES.new(self.key, AES.MODE_CBC, iv).decrypt(e[BS:])).decode() 

class CTR_cipher(cipher): 
    def __init__(self, key): 
        super().__init__(key)
        self.str = "CTR"
     
    def encrypt(self, pt): 
        pt = pad(pt.encode()) 
        ctr = Counter.new(BS * 8, initial_value=int.from_bytes(self.iv, byteorder='big'))
        ct = AES.new(self.key, AES.MODE_CTR, counter=ctr).encrypt(pt)
        res = self.iv + ct
        self.update_iv()
        return res
     
    def decrypt(self, e): 
        iv = e[:BS] 
        ctr = Counter.new(BS * 8, initial_value=int.from_bytes(iv, byteorder='big'))
        return unpad(AES.new(self.key, AES.MODE_CTR, counter=ctr).decrypt(e[BS:])).decode() 

class OFB_cipher(cipher): 
    def __init__(self, key): 
        super().__init__(key)
        self.str = "OFB"
     
    def encrypt(self, pt): 
        pt = pad(pt.encode()) 
        ct = AES.new(self.key, AES.MODE_OFB, self.iv).encrypt(pt)
        res = self.iv + ct
        self.update_iv()
        return res
     
    def decrypt(self, e): 
        iv = e[:BS] 
        return unpad(AES.new(self.key, AES.MODE_OFB, iv).decrypt(e[BS:])).decode() 
