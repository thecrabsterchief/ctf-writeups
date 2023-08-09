from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes as l2b
from Crypto.Util.Padding import pad

def recover_curve(P, Q, p):
    x0, y0 = P 
    x1, y1 = Q

    a, b = matrix(GF(p), [
        [x0, 1],
        [x1, 1]
    ]).solve_right(vector(GF(p), [y0^2 - x0^3, y1^2 - x1^3]))
    print(a,b,p)
    return EllipticCurve(GF(p), [a, b])

def recover_lcg(P, Q, p):
    E = recover_curve(P, Q, p)
    order = E.order()
    print(E)
    G = E.gens()[0]
    print(G)
    P = E(P)
    Q = E(Q)
    print(P)
    print(Q)
    # kp = discrete_log(P, G, operation='+')
    kp = 916472720818205535

    # kq = discrete_log(Q, G, operation='+')
    kq = 1673271260266693096

    # kp = a + b
    # kq = (a*kp + b)
    
    a, b = matrix(Zmod(order), [
        [1,  1],
        [kp, 1]
    ]).solve_right(vector(Zmod(order), [kp, kq]))

    return a*Q + b*G

x0 = 2029673067800379268
y0 = 1814239535542268363
x1 = 602316613633809952
y1 = 1566131331572181793
p  = 2525114415681006599
iv  = bytes.fromhex('6959dbf6bf22344d452c3831a3b68897')
enc = bytes.fromhex('a490e177c3838c8f24d36be5ee10e0c9e244ac2e54cd306eddfb0d585d5f27535835fab1cd83d26a669e6c08096b58cc4cc4cb082f4534ce80fab16e21f119adc45a5f59d179ca3683b77a942e4cf4081e01d921a51ec3a3a48c13f850c04b80c997367739bbde0a5415ff921d77a6ef')

if __name__ == "__main__":
    v   = recover_lcg(P=(x0,y0), Q=(x1,y1), p=p)
    
    v   = int(v.xy()[0])
    key = pad(l2b(v**2), 16)

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    flag = cipher.decrypt(enc)
    print(flag)

