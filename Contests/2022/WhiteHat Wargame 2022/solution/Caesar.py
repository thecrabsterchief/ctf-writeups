from string import *

low = ascii_lowercase
up = ascii_uppercase

enc = "SdepaDwp{g3i_yd@jd_d0_p3u}"
flag = ""

key = (ord("S") - ord("W")) % 26
for char in enc:
    if char in low:
        flag += low[(low.index(char) - key) % 26]
    elif char in up:
        flag += up[(up.index(char) - key) % 26]
    else:
        flag += char

print(flag)

# Flag: WhiteHat{k3m_ch@nh_h0_t3y}