import secrets
import nmKASUMI

# alpha = [0x0, 0x00100000]
alpha = 0x0000000000100000
# beta =  [0x00100000, 0x0]
beta = 0x0010000000000000
# gamma = [0x0, 0x00100000]
gamma = 0x0000000000100000
# delta = [0x00100000, 0x0]
delta = 0x0010000000000000
# deltaKab = [0x0, 0x0, 0x8000, 0x0, 0x0, 0x0, 0x0, 0x0]
deltaKab = 0x00000000800000000000000000000000
# deltaKac = [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x8000, 0x0]
deltaKac = 0x00000000000000000000000080000000

# E0 consists of rounds 1-3
E0 = 3
# M consists of round 4
# ME0 consists of rounds 1-4
ME0 = 4
# E1 consists of round 5-7
E1 = 7
# full consists of all 8 rounds
full = 8

#################################################################################################################
# start the for loop
for k in range(100000):
    print('k: ', k)

    #################################################################################################################
    # set up for PT a
    # create PT a
    Pa = secrets.token_hex(8)
    Pa = int(Pa, 16)
    # Pa = [Pa[:8], Pa[8:]]

    # create key for a
    Ka = secrets.token_hex(16)


    # calculate the value of Xa (semi encrypted through rounds 1-3)
    # calculate the value of Ya (semi encrypted through rounds 1-4)
    # also calculate the 7 round encryption Ca
    Ka = int(Ka, 16)
    Xa, Ya, Ca = nmKASUMI.sandwichEnc(Pa, Ka)
    # Ca = [Ca[:8], Ca[8:]]

    #################################################################################################################
    # set up for PT b
    # Pb = [None, None]
    # Pb[0] = format(int(Pa[0], 16) ^ alpha[0], 'x')
    # Pb[1] = format(int(Pa[1], 16) ^ alpha[1], 'x')
    Pb = Pa ^ alpha

    # create key for b
    # Kb = []
    # for i in range(len(Ka)):
    #     Kb.append((format(int(Ka[i], 16) ^ deltaKab[i], '04x')))
    
    Kb = Ka ^ deltaKab

    # calculate the value of Xb (semi encrypted through rounds 1-3)
    # calculate the value of Yb (semi encrypted through rounds 1-4)
    # also calculate the 7 round encryption Cb
    Xb, Yb, Cb = nmKASUMI.sandwichEnc(Pb, Kb)
    # Cb = [Cb[:8], Cb[8:]]

    #################################################################################################################
    # Shift Ca and Cb by delta to create Cc and Cd

    # Cc = [None, None]
    # Cc[0] = format(int(Ca[0], 16) ^ delta[0], 'x')
    # Cc[1] = format(int(Ca[1], 16) ^ delta[1], 'x')
    Cc = Ca ^ delta

    # Cd = [None, None]
    # Cd[0] = format(int(Cb[0], 16) ^ delta[0], 'x')
    # Cd[1] = format(int(Cb[1], 16) ^ delta[1], 'x')
    Cd = Cb ^ delta

    #################################################################################################################
    # create keys for Cc and Cd

    # Kc = []
    # for i in range(len(Ka)):
    #     Kc.append((format(int(Ka[i], 16) ^ deltaKac[i], '04x')))
    Kc = Ka ^ deltaKac

    # Kd = []
    # for i in range(len(Kc)):
    #     Kd.append((format(int(Kc[i], 16) ^ deltaKab[i], '04x')))
    Kd = Kc ^ deltaKab

    #################################################################################################################
    # Decrypt Cc and Cd for both full and E1 creating Pc, Pd and Yc, Yd resp

    Yc, Xc, Pc = nmKASUMI.sandwichDenc(Cc, Kc)
    Yd, Xd, Pd = nmKASUMI.sandwichDenc(Cd, Kd)

    #################################################################################################################
    # check conditions for right quartet-ness
    quartet = [0, 0, 0]

    # split up the X's so they can be XOR'd
    # Xa = [int(Xa[:32], 2), int(Xa[32:], 2)]
    # Xb = [int(Xb[:32], 2), int(Xb[32:], 2)]
    # Xc = [int(Xc[:32], 2), int(Xc[32:], 2)]
    # Xd = [int(Xd[:32], 2), int(Xd[32:], 2)]

    # # split up the Y's so they can be XOR'd
    # Ya = [int(Ya[:32], 2), int(Ya[32:], 2)]
    # Yb = [int(Yb[:32], 2), int(Yb[32:], 2)]
    # Yc = [int(Yc[:32], 2), int(Yc[32:], 2)]
    # Yd = [int(Yd[:32], 2), int(Yd[32:], 2)]

    # condition 1: Xa xor Xb == beta == Xc xor Xd
    # if (Xa[0] ^ Xb[0] == beta[0]) and (Xa[1] ^ Xb[1] == beta[1]) and (Xc[0] ^ Xd[0] == beta[0]) and (Xc[1] ^ Xd[1] == beta[1]):
    if ((Xa ^ Xb) == beta) and ((Xc ^ Xd) == beta):
        print('step 1 match')
        quartet[0] = 1
        # print('quartet: ', quartet)
    else:
        print('step 1 fail')
        # continue

    #  condition 2: Ya xor Yc == gamma
    # if (Ya[0] ^ Yc[0] == gamma[0]) and (Ya[1] ^ Yc[1] == gamma[1]):
    if (Ya ^ Yc == gamma) and (Yb ^ Yd == gamma):
        print('step 2 match')
        quartet[1] = 1
        # print('quartet: ', quartet)
    else:
        print('step 2 fail')
        # continue

    # condition 3: Ca xor Cc == delta == Cb xor Cd
    # if (Ca[0] ^ Cc[0] == delta[0]) and (Ca[1] ^ Cc[1] == delta[1]) and (Cb[0] ^ Cd[0] == delta[0]) and (Cb[1] ^ Cd[1] == delta[1]):
    if (Ca ^ Cc == delta) and (Cb ^ Cd == delta):
        print('step 3 match')
        quartet[2] = 1
        # print('quartet: ', quartet)
    else:
        print('step 3 fail')
        # continue

    print('quartet', quartet)
    if quartet == [1, 1, 1]:
        print('it works')
        print(Pa, Pb, Pc, Pd)
        print('Pa: ', hex(Pa))
        print('Pb: ', hex(Pb))
        print('Pc: ', hex(Pc))
        print('Pd: ', hex(Pd))
        check = (Pc ^ Pd) == alpha
        print(check)
        if check:
            break