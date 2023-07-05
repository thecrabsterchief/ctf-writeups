ct = "cb57ba706aae5f275d6d8941b7c7706fe261b7c74d3384390b691c3d982941ac4931c6a4394a1a7b7a336bc3662fd0edab3ff8b31b96d112a026f93fff07e61b"
stream = bytes.fromhex(ct)

flag = b'D'
for i in range(63):
    b  = stream[i] 
    b1 = flag[-1]
    b1 = (b1 ^ ((b1 << 1) | (b1 & 1))) & 0xff
    check = (b - b1) % 256 
    for b2 in range(256):
        if  (b2 ^ ((b2 >> 5) | (b2 << 3))) & 0xff == check:
            flag += bytes([b2])
            break

print(flag)
# DUCTF{i_d0nt_th1nk_th4ts_h0w_1t_w0rks_actu4lly_92f45fb961ecf420}
