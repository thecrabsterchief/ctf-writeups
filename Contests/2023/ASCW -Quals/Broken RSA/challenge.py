inv_q = pow(rsa.q, -1, rsa.p)
def sign():
    message = getrandbits(256)

    sp1 = pow(message, int(rsa._dp), rsa.p)
    sq1 = pow(message, int(rsa._dq), rsa.q) + getrandbits(256)
    s = sq1 + rsa.q*(inv_q * (sp1 - sq1) % rsa.p)

    return message, s