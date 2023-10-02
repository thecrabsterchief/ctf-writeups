import string
import random

ALPHABET = string.ascii_uppercase


def generate_key():
    return [random.randint(0, 26) for _ in range(13)]

def generate_keystream(key, length):
    keystream = []
    while len(keystream) < length:
        keystream.extend(key)
        key = key[1:] + key[:1]
    return keystream

def decrypt(message, key):
    indices = [ALPHABET.index(c) if c in ALPHABET else c for c in message.upper()]
    keystream = generate_keystream(key, len(message))
    decrypted = []

    for i in range(len(indices)):
        if isinstance(indices[i], int):
            if keystream[i] != -1:
                decrypted.append(ALPHABET[(-keystream[i] + indices[i]) % 26])
            else:
                decrypted.append("?")
        else:
            decrypted.append(indices[i])

    return "".join(decrypted)

if __name__ == "__main__":
    ct = open("./ciphertext.txt", "r").read()

    while True:
        key = list(map(int, input("Enter key: ").split()))
        assert len(key) == 13

        print("="*100)
        print(decrypt(ct, key))
        print("="*100)

# key: 12 21 8 19 8 8 19 23 15 12 25 16 12