# https://github.com/bozhu/GOST-Python/tree/master

sbox = (
    (4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3),
    (14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9),
    (5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11),
    (7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3),
    (6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2),
    (4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14),
    (13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12),
    (1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12),
)

# sbox = (
#     (12,4,6,2,10,5,11,9,14,8,13,7,0,3,15,1),
#     (6,8,2,3,9,10,5,12,1,14,4,7,11,13,0,15),
# (11,3,5,8,2,15,10,13,14,1,7,4,12,9,6,0),
# (12,8,2,1,13,4,15,6,7,0,10,5,3,14,9,11),
# (7,15,5,10,8,1,6,13,0,9,3,14,11,4,2,12),
# (5,13,15,6,9,2,12,10,11,7,8,1,4,3,14,0),
# (8,14,2,5,6,9,1,12,15,4,11,0,13,10,3,7),
# (1,7,14,13,0,5,8,3,4,15,10,6,9,12,11,2)
# )


def _bit_length(x):
    assert x >= 0
    return len(bin(x)) - 2


def f_function(var, key):
    assert _bit_length(var) <= 32
    assert _bit_length(key) <= 32

    temp = (var + key) % (1 << 32)
    # print('temp: ', hex(temp))

    output = 0
    for i in range(8):
        output |= ((sbox[i][(temp >> (4 * i)) & 0b1111]) << (4 * i))
        # output |= ((sbox[i][(temp >> (4 * (7 - i))) & 0b1111]) << (4 * i))

    output = ((output >> (32 - 11)) | (output << 11)) & 0xFFFFFFFF

    return output


def round_encryption(input_left, input_right, round_key):
    output_left = input_right
    output_right = input_left ^ f_function(input_right, round_key)

    return output_left, output_right


def round_decryption(input_left, input_right, round_key):
    output_right = input_left
    output_left = input_right ^ f_function(input_left, round_key)

    return output_left, output_right


class GOST:
    def __init__(self):
        self.master_key = [None] * 8

    def set_key(self, master_key):
        assert _bit_length(master_key) <= 256
        for i in range(8):
            # self.master_key[i] = (master_key >> (32 * i)) & 0xFFFFFFFF
            self.master_key[i] = (master_key >> (32 * (7 - i))) & 0xFFFFFFFF
        # print 'master_key', [hex(i) for i in self.master_key]

    def encrypt(self, plaintext):
        assert _bit_length(plaintext) <= 64
        text_left = plaintext >> 32
        text_right = plaintext & 0xFFFFFFFF

        for i in range(24):
            # print('mid round ', i, ' : ', hex(text_left << 32 | text_right))
            # print('master key: ', hex(self.master_key[i % 8]))
            text_left, text_right = round_encryption(
                text_left, text_right, self.master_key[i % 8])

        X = text_left << 32 | text_right
        

        for i in range(8):
            if i==0:
                z = text_left << 32 | text_right
                # print('before: ', hex(text_left), hex(text_right))
                before = text_left << 32 | text_right
            # print('mid round ', i, ' : ', hex(text_left << 32 | text_right))
            # print('master key: ', hex(self.master_key[7-i]))
            # print('master key: ', (self.master_key))
            
            text_left, text_right = round_encryption(
                text_left, text_right, self.master_key[7 - i])
            
            if i ==0:
                # print('after: ', hex(text_left), hex(text_right))
                after = text_left << 32 | text_right

        
        # print('z: ', hex(z))
        # print('beta flipped: ', hex(0x8000000000000000))

        return (text_right << 32) | text_left, X, z, before, after

    def decrypt(self, ciphertext):
        assert _bit_length(ciphertext) <= 64
        text_right = ciphertext >> 32
        text_left = ciphertext & 0xFFFFFFFF

        for i in range(8):
            
            # print('master key: ', hex(self.master_key[i]))
            text_left, text_right = round_decryption(
                text_left, text_right, self.master_key[i])
            
            # print('mid round ', i, ' : ', hex(text_left << 32 | text_right))

        X = text_left << 32 | text_right

        for i in range(24):
            # print('mid round ', i, ' : ', hex(text_left << 32 | text_right))
            # print('master key: ', hex(self.master_key[(7-i) % 8]))
            text_left, text_right = round_decryption(
                text_left, text_right, self.master_key[(7 - i) % 8])

        return (text_left << 32) | text_right, X
    
    def semiEncrypt(self, plaintext):
        assert _bit_length(plaintext) <= 64
        text_left = plaintext >> 32
        text_right = plaintext & 0xFFFFFFFF

        for i in range(8):
            text_left, text_right = round_encryption(
                text_left, text_right, self.master_key[7 - i])

        return (text_right << 32) | text_left
    
    def semiDecrypt(self, plaintext):
        assert _bit_length(plaintext) <= 64
        text_right = plaintext >> 32
        text_left = plaintext & 0xFFFFFFFF

        for i in range(8):
            text_left, text_right = round_encryption(
                text_left, text_right, self.master_key[i])

        return (text_left << 32) | text_right
    
    def semiEncryptStart(self, plaintext):
        assert _bit_length(plaintext) <= 64
        text_left = plaintext >> 32
        text_right = plaintext & 0xFFFFFFFF

        for i in range(24):
            text_left, text_right = round_encryption(
                text_left, text_right, self.master_key[i % 8])

        return (text_left << 32) | text_right
    
    def semiDecryptStart(self, ciphertext):
        assert _bit_length(ciphertext) <= 64
        text_left = ciphertext >> 32
        text_right = ciphertext & 0xFFFFFFFF

        for i in range(24):
            text_left, text_right = round_decryption(
                text_left, text_right, self.master_key[(7 - i) % 8])

        return (text_left << 32) | text_right


def og():
    # text = 0xfedcba0987654321
    # key = 0x1111222233334444555566667777888899990000aaaabbbbccccddddeeeeffff

    text = 0xfedcba9876543210
    key = 0xffeeddccbbaa99887766554433221100f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff

    my_GOST = GOST()
    my_GOST.set_key(key)

    # num = 1000

    # for i in range(num):
    text, X = my_GOST.encrypt(text)
    # print('enc: ', hex(text))
    # print('Xe: ', hex(X))

    # for i in range(num):
    text, X = my_GOST.decrypt(text)
    # print('dec: ', hex(text))
    # print('Xde: ', hex(X))

# og()

def BoomEnc(text, key):
    myGOST = GOST()
    myGOST.set_key(key)

    C, X, z, before, after = myGOST.encrypt(text)

    return X, C, z, before, after

def BoomDec(text, key):
    myGOST = GOST()
    myGOST.set_key(key)

    P, X = myGOST.decrypt(text)

    return X, P

def semiE(text, key):
    myGOST = GOST()
    myGOST.set_key(key)

    C = myGOST.semiEncrypt(text)

    return C

def semiD(text, key):
    myGOST = GOST()
    myGOST.set_key(key)

    P = myGOST.semiDecrypt(text)

    return P

def semiES(text, key):
    myGOST = GOST()
    myGOST.set_key(key)

    C = myGOST.semiEncryptStart(text)

    return C

def semiDS(text, key):
    myGOST = GOST()
    myGOST.set_key(key)

    P = myGOST.semiDecryptStart(text)

    return P


def test():
    val = round_encryption(0, 0x80000000, 0)
    print(hex(val[0]), hex(val[1]))
    
# test()