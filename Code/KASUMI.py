def ROL16(a, b):
    return ((a << b) | (a >> (16 - b))) & 0xFFFF


# globals: the subkey arrays

KLi1 = [None] * 8
KLi2 = [None] * 8
KOi1 = [None] * 8
KOi2 = [None] * 8
KOi3 = [None] * 8
KIi1 = [None] * 8
KIi2 = [None] * 8
KIi3 = [None] * 8


def FI(inp, subkey):

    S7 = [54, 50, 62, 56, 22, 34, 94, 96, 38, 6, 63, 93, 2, 18,123, 33,
		55,113, 39,114, 21, 67, 65, 12, 47, 73, 46, 27, 25,111,124, 81,
		53, 9,121, 79, 52, 60, 58, 48,101,127, 40,120,104, 70, 71, 43,
		20,122, 72, 61, 23,109, 13,100, 77, 1, 16, 7, 82, 10,105, 98,
		117,116, 76, 11, 89,106, 0,125,118, 99, 86, 69, 30, 57,126, 87,
		112, 51, 17, 5, 95, 14, 90, 84, 91, 8, 35,103, 32, 97, 28, 66,
		102, 31, 26, 45, 75, 4, 85, 92, 37, 74, 80, 49, 68, 29,115, 44,
		64,107,108, 24,110, 83, 36, 78, 42, 19, 15, 41, 88,119, 59, 3]

    S9 = [167,239,161,379,391,334,  9,338, 38,226, 48,358,452,385, 90,397,
		183,253,147,331,415,340, 51,362,306,500,262, 82,216,159,356,177,
		175,241,489, 37,206, 17,  0,333, 44,254,378, 58,143,220, 81,400,
		95,  3,315,245, 54,235,218,405,472,264,172,494,371,290,399, 76,
		165,197,395,121,257,480,423,212,240, 28,462,176,406,507,288,223,
		501,407,249,265, 89,186,221,428,164, 74,440,196,458,421,350,163,
		232,158,134,354, 13,250,491,142,191, 69,193,425,152,227,366,135,
		344,300,276,242,437,320,113,278, 11,243, 87,317, 36, 93,496, 27,
		487,446,482, 41, 68,156,457,131,326,403,339, 20, 39,115,442,124,
		475,384,508, 53,112,170,479,151,126,169, 73,268,279,321,168,364,
		363,292, 46,499,393,327,324, 24,456,267,157,460,488,426,309,229,
		439,506,208,271,349,401,434,236, 16,209,359, 52, 56,120,199,277,
		465,416,252,287,246,  6, 83,305,420,345,153,502, 65, 61,244,282,
		173,222,418, 67,386,368,261,101,476,291,195,430, 49, 79,166,330,
		280,383,373,128,382,408,155,495,367,388,274,107,459,417, 62,454,
		132,225,203,316,234, 14,301, 91,503,286,424,211,347,307,140,374,
		35,103,125,427, 19,214,453,146,498,314,444,230,256,329,198,285,
		50,116, 78,410, 10,205,510,171,231, 45,139,467, 29, 86,505, 32,
		72, 26,342,150,313,490,431,238,411,325,149,473, 40,119,174,355,
		185,233,389, 71,448,273,372, 55,110,178,322, 12,469,392,369,190,
        1,109,375,137,181, 88, 75,308,260,484, 98,272,370,275,412,111,
		336,318,  4,504,492,259,304, 77,337,435, 21,357,303,332,483, 18,
		47, 85, 25,497,474,289,100,269,296,478,270,106, 31,104,433, 84,
		414,486,394, 96, 99,154,511,148,413,361,409,255,162,215,302,201,
		266,351,343,144,441,365,108,298,251, 34,182,509,138,210,335,133,
		311,352,328,141,396,346,123,319,450,281,429,228,443,481, 92,404,
		485,422,248,297, 23,213,130,466, 22,217,283, 70,294,360,419,127,
		312,377,  7,468,194,  2,117,295,463,258,224,447,247,187, 80,398,
		284,353,105,390,299,471,470,184, 57,200,348, 63,204,188, 33,451,
		97, 30,310,219, 94,160,129,493, 64,179,263,102,189,207,114,402,
		438,477,387,122,192, 42,381,  5,145,118,180,449,293,323,136,380,
        43, 66, 60,455,341,445,202,432, 8,237, 15,376,436,464, 59,461]
    
    # print('inp', inp)
    nine = (inp >> 7)
    seven = inp & 0x7F
	
    # print('nine', nine)

    nine = S9[nine] ^ seven
    seven = S7[seven] ^ (nine & 0x7F)
    
    seven ^= subkey >> 9
    nine ^= subkey & 0x1FF

    nine = S9[nine] ^ seven
    seven = S7[seven] ^ (nine & 0x7F)
	
    inp = (seven << 9) + nine
	
    return inp

def FO(inp, index):
    
    inp = format(inp, '032b')

    # print('inp FO', inp)
    left = inp[:16]
    # print('left FO', left)
    right = inp[16:]
    # print('right FO', right)
    left = int(left, 2)
    right = int(right, 2)
    
    left ^= KOi1[index]
    # print('left FO 2.1', left)
    left = FI(left, KIi1[index])
    # print('left FO 2.2', left)
    left ^= right
    # print('left FO 2.3', left)
    
    # print('KOi2[index]', format(KOi2[index], '0{}b'.format(32)))
    # print('right bin =', format(right, 'b'))
    right ^= KOi2[index]
    # print('right FO 3.1', right)
    right = FI(right, KIi2[index])
    # print('right FO 3.2', right)
    right ^= left
    
    left ^= KOi3[index]
    left = FI(left, KIi3[index])
    left ^= right
    
    inp = (right << 16) + left
    
    return inp

def FL(inp, index):
    
    inp = format(inp, '032b')
    # print('inp FL', inp)
    l = inp[:16]
    r = inp[16:]
    # print('l', l)
    # print('r', r)
    l = int(l, 2)
    r = int(r, 2)
    
    
    a = l & KLi1[index]
    # print('a', format(a, 'b'))
    r ^= ROL16(a, 1)
    # print('r', format(r, 'b'))
    b = r | KLi2[index]
    l ^= ROL16(b, 1)
    
    
    
    inp = (l << 16) + r
    
    return inp

def KASUMI(data, round):
    
    # d = DWORD(data)
    # print(d)
    # print(f"32-bit values: 0x{d.b32[0]:08X} 0x{d.b32[1]:08X}")
    
    # left = ((d[0].b8[0]) << 24) + ((d[0].b8[1]) << 16) + (d[0].b8[2] << 8) + (d[0].b8[3])
    
    # right = ((d[1].b8[0]) << 24) + ((d[1].b8[1]) << 16) + (d[1].b8[2] << 8) + (d[1].b8[3])
    
    # d = INPWORD(data)
    
    # left = d.b32[0]
    # right = d.b32[1]

    # d = [data[:32], data[32:]]
    d = data
    # print('d', d)
    # print(d[0][0][:8])
    # left = [[d[0][0][:8]], [d[0][0][8:16]], [d[0][0][16:24]], [d[0][0][24:]]]
    left = d[0]
    # print(left)
    left = int(left, 16)
    # right = [[d[1][0][:8]], [d[1][0][8:16]], [d[1][0][16:24]], [d[1][0][24:]]]
    right = d[1]
    # print(right)
    right = int(right, 16)
    # print(KLi1)
    
    # OG KASUMI loop
    # n = 0
    # while n <= 7:
    #     temp = FL(left, n)
    #     # print('temp FL', hex(temp))
    #     temp = FO(temp, n)
    #     print('temp FO', hex(temp))
    #     print(hex(left))
    #     print('right before', hex(right))
    #     right ^= temp
    #     print('right', hex(right))
    #     n += 1
    #     # print('right while 2', right)
    #     temp = FO(right, n)
    #     temp = FL(temp, n)
    #     left ^= temp
    #     n += 1
    if round == 3:
        # ROUND 1
        n = 0
        temp = FL(left, n)
        temp = FO(temp, n)
        right ^= temp
        
        n += 1
        # ROUND 2
        temp = FO(right, n)
        temp = FL(temp, n)
        left ^= temp
        n += 1
        # ROUND 3
        temp = FL(left, n)
        temp = FO(temp, n)
        right ^= temp 
    elif round == 4:
        # print('KLi1', KLi1)
        # ROUND 1
        n = 0
        temp = FL(left, n)
        temp = FO(temp, n)
        right ^= temp
        
        n += 1
        # ROUND 2
        temp = FO(right, n)
        temp = FL(temp, n)
        left ^= temp
        n += 1
        # ROUND 3
        temp = FL(left, n)
        temp = FO(temp, n)
        right ^= temp 
        # ROUND 4
        n += 1
        temp = FO(right, n)
        temp = FL(temp, n)
        left ^= temp
    elif round == 7:
        # ROUND 5
        n = 5
        temp = FL(left, n)
        temp = FO(temp, n)
        right ^= temp
        n += 1
        # ROUND 6
        temp = FO(right, n)
        temp = FL(temp, n)
        left ^= temp
        n += 1
        # ROUND 7
        temp = FL(left, n)
        temp = FO(temp, n)
        right ^= temp
    elif round == -7:
        n = 7
        # ROUND 7
        temp = FL(right, n)
        temp = FO(temp, n)
        left ^= temp
        n -= 1
        
        # ROUND 6
        temp = FO(left, n)
        temp = FL(temp, n)
        right ^= temp
        n -= 1

        # ROUND 5
        temp = FL(right, n)
        temp = FO(temp, n)
        left ^= temp
    elif round == -8:
        n = 8
        while n <= 0:
            temp = FL(right, n)
            temp = FO(temp, n)
            left ^= temp
            n -= 1
            temp = FO(left, n)
            temp = FL(temp, n)
            right ^= temp
            n -= 1
    else:
        n = 0
        while n <= 7:
            temp = FL(left, n)
            # print('temp FL', hex(temp))
            temp = FO(temp, n)
            # print('temp FO', hex(temp))
            # print(hex(left))
            # print('right before', hex(right))
            right ^= temp
            # print('right', hex(right))
            n += 1
            # print('right while 2', right)
            temp = FO(right, n)
            temp = FL(temp, n)
            left ^= temp
            n += 1

    
    # d[0].b8[0] = left >> 24
    # d[0].b8[1] = left >> 16
    # d[0].b8[2] = left >> 8
    # d[0].b8[3] = left
    # d[1].b8[3] = right
    # d[1].b8[2] = right >> 8
    # d[1].b8[1] = right >> 16
    # d[1].b8[0] = right >> 24
    
    


    output = format(left, '032b') + format(right, '032b')
    # print(format(left, '032b'), format(right, '032b'))
    # print(output)

    return output

def KeySchedule(key):
    
    c = [0x0123, 0x4567, 0x89AB, 0xCDEF, 0xFEDC, 0xBA98, 0x7654, 0x3210]
    
    # key = [None] * 8
    Kprime = [None] * 8
    
    # k16 = WORD(k)
    # # print(k)
    # key = [k[:16], k[16:32], k[32:48], k[48:64], 
    #     k[64:80], k[80:96], k[96:112], k[112:]]
    # print(key)
    
    for n in range(0, 8):
        # print(key[n][0])
        Kprime[n] = int(key[n], 16) ^ c[n]
    
    for n in range(0, 8):
        KLi1[n] = ROL16(int(key[n], 16),1)
        KLi2[n] = Kprime[(n+2)&0x7]
        KOi1[n] = ROL16(int(key[(n+1)&0x7], 16),5)
        KOi2[n] = ROL16(int(key[(n+5)&0x7], 16),8)
        KOi3[n] = ROL16(int(key[(n+6)&0x7], 16),13)
        KIi1[n] = Kprime[(n+4)&0x7]
        KIi2[n] = Kprime[(n+3)&0x7]
        KIi3[n] = Kprime[(n+7)&0x7]
    
    sandwichKey = [KLi1, KLi2, KOi1, KOi2, KOi3, KIi1, KIi2, KIi3]
    return sandwichKey


# key = 0x9900aabbccddeeff1122334455667788 # 128-bit
# key = format(key, '0128b')
# KeySchedule(key)

# # # print('KOi1')
# # # for block in KOi1:
# # #     print(hex(block))

# plainText = 0xfedcba0987654321 # 64-bit
# plainText = format(plainText, '064b')
# print('pt', hex(int(plainText, 2)))
# cipherText = 0x514896226caa4f20


# answer = KASUMI(plainText, 8)
# decAns = KASUMI(plainText, -8)
# print('ans', hex(int(answer, 2)))
# print('decans', hex(int(decAns, 2)))
# print(hex(cipherText))
# assert hex(cipherText) == hex(int(answer, 2)), "Ruh Roh"