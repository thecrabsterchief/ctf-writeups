import requests
import HashTools # pip install length-extension-tool
from tqdm import tqdm

given = bytes.fromhex("675f4f4e143f87d0068550413aa77deac2853f33e928b69230c8ec6a749d8a")

for i in tqdm(range(256)):
    full_hash = (bytes([i]) + given).hex()
    magic = HashTools.new("sha256")
    new_data, new_signature = magic.extension(secret_length=16, original_data=b"", append_data=b"vnc", signature=full_hash)
    new_data = "00"*15 + "0a" + new_data.hex()

    # url = "http://127.0.0.1:5000/getf?table=flag_table&hash=" + new_signature + "&id=" + new_data
    url = "http://litctf.org:31773/getf?table=flag_table&hash=" + new_signature + "&id=" + new_data
    
    res = requests.get(url)
    if "ERR" not in res.text:
        print(url)
        print(res.text)
        exit(0)
