import string

ct = "rtkw{cf0bj_czbv_nv'cc_y4mv_kf_kip_re0kyvi_uivjj1ex_5vw89s3r44901831}"

def solve(ct, shift):
    flag = ""
    for i in ct:
        if i in string.ascii_lowercase:
            flag += chr(((ord(i) - 97 + shift) % 26)+97)
        else:
            flag += i
    return flag

if __name__ == "__main__":
    for shift in range(26):
        flag = solve(ct, shift)
        if flag.startswith("actf{"):
            print("Flag:", flag)
            exit()