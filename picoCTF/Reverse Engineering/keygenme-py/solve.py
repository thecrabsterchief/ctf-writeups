from hashlib import sha256

bUsername_trial = b"FREEMAN"

key_part_static1_trial = "picoCTF{1n_7h3_|<3y_of_"
key_part_dynamic1_trial = "xxxxxxxx"
key_part_static2_trial = "}"
key_full_template_trial = key_part_static1_trial + key_part_dynamic1_trial + key_part_static2_trial

indexs = [4, 5, 3, 6, 2, 7, 1, 8]
key = ""

for i in indexs:
    key += sha256(bUsername_trial).hexdigest()[i]

flag = key_part_static1_trial + key + key_part_static2_trial
print(flag)
