def spiralRight(matrix):
    right = []
    for j in range(4):
        for i in range(3, -1, -1):
            right.append(matrix[i][j])
    return bytes2matrix(right)


# rotate a 4x4 matrix counterclockwise
def spiralLeft(matrix):
    left = []
    for j in range(3, -1, -1):
        for i in range(4):
            left.append(matrix[i][j])
    return bytes2matrix(left)


# convert bytes to 4x4 matrix
def bytes2matrix(bytes):
    return [list(bytes[i : i + 4]) for i in range(0, len(bytes), 4)]


# convert 4x4 matrix to bytes
def matrix2bytes(matrix):
    return bytes(sum(matrix, []))

SBOX = [184, 79, 76, 49, 237, 28, 54, 183, 106, 24, 192, 7, 43, 111, 175, 44, 46, 199, 182, 115, 83, 227, 61, 230, 6, 57, 165, 137, 58, 14, 94, 217, 66, 120, 53, 142, 29, 150, 103, 75, 186, 39, 31, 196, 18, 207, 244, 16, 213, 243, 114, 251, 96, 4, 138, 197, 10, 176, 157, 91, 238, 155, 254, 71, 86, 37, 130, 12, 52, 162, 220, 56, 88, 188, 27, 208, 25, 51, 172, 141, 168, 253, 85, 193, 90, 35, 95, 105, 200, 127, 247, 21, 93, 67, 13, 235, 84, 190, 225, 119, 189, 81, 250, 117, 231, 50, 179, 22, 223, 26, 228, 132, 139, 166, 210, 23, 64, 108, 212, 201, 99, 218, 160, 240, 129, 224, 233, 242, 159, 47, 126, 125, 146, 229, 0, 252, 161, 98, 30, 63, 239, 164, 36, 80, 151, 245, 38, 107, 3, 65, 73, 204, 8, 205, 82, 78, 173, 112, 219, 136, 123, 149, 118, 32, 215, 163, 74, 134, 248, 68, 110, 45, 59, 145, 178, 156, 100, 177, 221, 2, 92, 20, 40, 144, 101, 140, 169, 116, 143, 202, 1, 113, 209, 104, 133, 128, 70, 89, 216, 147, 122, 131, 9, 249, 121, 109, 191, 77, 124, 246, 55, 198, 187, 185, 17, 60, 180, 203, 19, 158, 97, 206, 148, 5, 87, 170, 236, 222, 194, 15, 214, 241, 211, 234, 42, 41, 153, 62, 102, 152, 69, 181, 34, 48, 226, 11, 195, 154, 174, 167, 135, 232, 72, 171, 33]

SPIRAL = [
    [1, 19, 22, 23],
    [166, 169, 173, 31],
    [149, 212, 176, 38],
    [134, 94, 59, 47],
]

INV_SPIRAL = [
    [ 92, 218, 173, 241],
    [ 24,  21, 217, 233],
    [ 54, 142, 124, 192],
    [235,  48, 127, 201]
]

class Spiral:
    def __init__(self, key, rounds=4):
        self.rounds = rounds
        self.keys = [bytes2matrix(key)]
        self.BLOCK_SIZE = 16

        for i in range(rounds):
            self.keys.append(spiralLeft(self.keys[-1]))

    def encrypt(self, plaintext):
        if len(plaintext) % self.BLOCK_SIZE != 0:
            padding = self.BLOCK_SIZE - len(plaintext) % self.BLOCK_SIZE
            plaintext += bytes([padding] * padding)

        ciphertext = b""
        for i in range(0, len(plaintext), 16):
            ciphertext += self.encrypt_block(plaintext[i : i + 16])
        return ciphertext

    def encrypt_block(self, plaintext):
        self.state = bytes2matrix(plaintext)
        self.add_key(0)

        for i in range(1, self.rounds):
            self.substitute()
            self.rotate()
            self.mix()
            self.add_key(i)

        self.substitute()
        self.rotate()
        self.add_key(self.rounds)

        return matrix2bytes(self.state)

    def add_key(self, idx):
        for i in range(4):
            for j in range(4):
                self.state[i][j] = (self.state[i][j] + self.keys[idx][i][j]) % 255

    def substitute(self):
        for i in range(4):
            for j in range(4):
                self.state[i][j] = SBOX[self.state[i][j]]

    def rotate(self):
        self.state = spiralRight(self.state)

    def mix(self):
        out = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    out[i][j] += SPIRAL[i][k] * self.state[k][j]
                out[i][j] %= 255

        self.state = out

    def decrypt(self, ciphertext):
        plaintext = b""
        for i in range(0, len(ciphertext), 16):
            plaintext += self.decrypt_block(ciphertext[i:i+16])
        return plaintext
    
    def decrypt_block(self, ciphertext):
        self.state = bytes2matrix(ciphertext)
        
        self.rev_add_key(self.rounds)
        self.rev_rotate()
        self.rev_substitute()

        for i in range(self.rounds - 1, 0, -1):
            self.rev_add_key(i)
            self.rev_mix()
            self.rev_rotate()
            self.rev_substitute()
        
        self.rev_add_key(0)
        return matrix2bytes(self.state)
    def rev_add_key(self, idx):
        for i in range(4):
            for j in range(4):
                self.state[i][j] = (self.state[i][j] - self.keys[idx][i][j]) % 255

    def rev_substitute(self):
        for i in range(4):
            for j in range(4):
                self.state[i][j] = SBOX.index(self.state[i][j])

    def rev_rotate(self):
        self.state = spiralLeft(self.state)
    
    def rev_mix(self):
        out = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    out[i][j] += INV_SPIRAL[i][k] * self.state[k][j]
                out[i][j] %= 255

        self.state = out
