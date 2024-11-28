import secrets
import KASUMI

alpha = [0x0, 0x00100000]
beta =  [0x00100000, 0x0]
gamma = [0x0, 0x00100000]
delta = [0x00100000, 0x0]
deltaKab = [0x0, 0x0, 0x8000, 0x0, 0x0, 0x0, 0x0, 0x0]
deltaKac = [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x8000, 0x0]

isRightQuartet = False
numTries = 0

# E0 consists of rounds 1-3
E0 = 3
# M consists of round 4
M = 4
# E1 consists of round 5-7
E1 = 7
# full consists of all 8 rounds
full = 8

while isRightQuartet == False:
    rightness = [0, 0, 0]
    numTries += 1
    Pa = secrets.token_hex(8)
    Pa = [Pa[:8], Pa[8:]]
    # print('Pa', Pa)
    Pb = [None, None]
    Pb[0] = format(int(Pa[0], 16) ^ alpha[0], 'x')
    Pb[1] = format(int(Pa[1], 16) ^ alpha[1], 'x')
    # print('Pb', Pb)

    Pc = secrets.token_hex(8)
    Pc = [Pc[:8], Pc[8:]]
    # print('Pc', Pc)
    Pd = [None, None]
    Pd[0] = format(int(Pc[0], 16) ^ alpha[0], 'x')
    Pd[1] = format(int(Pc[1], 16) ^ alpha[1], 'x')
    # print('Pd', Pd)


    Ka = secrets.token_hex(16)
    # print('Ka', Ka)
    Ka = [Ka[:4], Ka[4:8], Ka[8:12], Ka[12:16], Ka[16:20], Ka[20:24], Ka[24:28], Ka[28:]]
    # print('Ka', Ka)
    # print('Kab', deltaKab)
    Kb = []
    for i in range(len(Ka)):
        Kb.append((format(int(Ka[i], 16) ^ deltaKab[i], '04x')))
    # print('Kb', Kb)

    Kc = []
    for i in range(len(Ka)):
        Kc.append((format(int(Ka[i], 16) ^ deltaKac[i], '04x')))
    # print('Kc', Kc)

    Kd = []
    for i in range(len(Kc)):
        Kd.append((format(int(Kc[i], 16) ^ deltaKab[i], '04x')))
    # print('Kd', Kd)


    E0Ka = KASUMI.KeySchedule(Ka)
    # print('E0Ka[0]', E0Ka[0])
    E0KaPa = KASUMI.KASUMI(Pa, E0)
    E0KaPa = [int(E0KaPa[:32], 2), int(E0KaPa[32:], 2)]
    # print('E0KaPa', E0KaPa)

    E0Kb = KASUMI.KeySchedule(Kb)
    # print(E0Kb[0])
    E0KbPb = KASUMI.KASUMI(Pb, E0)
    E0KbPb = [int(E0KbPb[:32], 2), int(E0KbPb[32:], 2)]

    E0Kc = KASUMI.KeySchedule(Kc)
    # print('E0Kc[0]', E0Kc[0])
    E0KcPc = KASUMI.KASUMI(Pc, E0)
    E0KcPc = [int(E0KcPc[:32], 2), int(E0KcPc[32:], 2)]
    # print('E0KcPc', E0KcPc)

    E0Kd = KASUMI.KeySchedule(Kd)
    # print(E0Kd[0])
    E0KdPd = KASUMI.KASUMI(Pd, E0)
    E0KdPd = [int(E0KdPd[:32], 2), int(E0KdPd[32:], 2)]


    # if (E0KaPa[0] ^ E0KbPb[0] == beta[1]) and (E0KaPa[1] ^ E0KbPb[1] == beta[0]) and (E0KcPc[0] ^ E0KdPd[0] == beta[1]) and (E0KcPc[1] ^ E0KdPd[1] == beta[0]):
    #     rightness[0] = 1
    #     print('stage 1: ', rightness)

    # if rightness[0] == 1:
    # print('in stage 2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        
    # print(E0KaPa[0], E0KcPc[0], E0KaPa[0] ^ E0KcPc[0], gamma[1])
    # print(E0KaPa[1], E0KcPc[1], E0KaPa[1] ^ E0KcPc[1], gamma[0])
    
    # print(E0KbPb[0], E0KdPd[0], E0KbPb[0] ^ E0KdPd[0], gamma[1])
    # print(E0KbPb[1], E0KdPd[1], E0KbPb[1] ^ E0KdPd[1], gamma[0])
    
    if (E0KbPb[0] ^ E0KdPd[0] == gamma[1]) and (E0KbPb[1] ^ E0KdPd[1] == gamma[0]):
        rightness[1] = 1
        print('the implied statement is correct')
        
    if (E0KaPa[0] ^ E0KcPc[0] == gamma[1]) and (E0KaPa[1] ^ E0KcPc[1] == gamma[0]):
        rightness[1] = 1
        print('stage 2: ', rightness)

    if rightness[1] == 1:
        KASUMI.KeySchedule(Ka)
        Ca = KASUMI.KASUMI(Pa, full)
        Ca = [int(Ca[:32], 2), int(Ca[32:], 2)]

        KASUMI.KeySchedule(Kb)
        Cb = KASUMI.KASUMI(Pb, full)
        Cb = [int(Cb[:32], 2), int(Cb[32:], 2)]

        KASUMI.KeySchedule(Kc)
        Cc = KASUMI.KASUMI(Pc, full)
        Cc = [int(Cc[:32], 2), int(Cc[32:], 2)]

        KASUMI.KeySchedule(Kd)
        Cd = KASUMI.KASUMI(Pd, full)
        Cd = [int(Cd[:32], 2), int(Cd[32:], 2)]

        if (Ca[0] ^ Cc[0] == delta[0]) and (Ca[1] ^ Cc[1] == delta[1]) and (Cb[0] ^ Cd[0] == delta[0]) and (Cb[1] ^ Cd[1] == delta[1]):
            rightness[2] = 1
            print('stage 3: ', rightness)

    isRightQuartet = all(element == 1 for element in rightness)
    print(isRightQuartet, numTries)

print('a right quartet: [', Pa, ', ', Pb, ', ', Pc, ', ', Pd, ']')
