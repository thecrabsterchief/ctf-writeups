import requests

ct  = "1_c_3_c_0__ff_3e"
org = 0

for i in range(0, 16):
    if ct[i].isnumeric():
        res = int(ct[i])
    elif ct[i] == "_":
        res = 11
    else:
        res = int(ct[i], 16)
    
    org = (org << 4) + res

poc = requests.post(url="http://host3.dreamhack.games:18474/", data={
    "menu_input": str(org)
})

print(poc.text)