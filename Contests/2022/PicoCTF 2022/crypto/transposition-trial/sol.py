ciphertext = "heTfl g as iicpCTo{7F4NRP051N5_16_35P3X51N3_V9AAB1F8}7"
blocks = [ciphertext[i:i + 3] for i in range(0, len(ciphertext), 3)]

message = ""

for block in blocks:
    message += block[-1] + block[:-1]

print(message)

# The flag is picoCTF{7R4N5P051N6_15_3XP3N51V3_A9AFB178}