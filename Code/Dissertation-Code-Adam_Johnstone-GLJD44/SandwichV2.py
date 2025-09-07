import secrets
import nmKASUMI

alpha = 0x0000000000100000
beta = 0x0010000000000000
gamma = 0x0000000000100000
delta = 0x0010000000000000
deltaKab = 0x00000000800000000000000000000000
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
    # Pa = '830397a70b30a01a'
    Pa = int(Pa, 16)

    # create key for a
    Ka = secrets.token_hex(16)
    # Ka = 'ce8ec6aa3b8a91255690849596899ea9'


    # calculate the value of Xa (semi encrypted through rounds 1-3)
    # calculate the value of Ya (semi encrypted through rounds 1-4)
    # also calculate the 7 round encryption Ca
    Ka = int(Ka, 16)
    Xa, Ya, Ca = nmKASUMI.sandwichEnc(Pa, Ka)

    #################################################################################################################
    # set up for PT b
    # create PT b
    Pb = Pa ^ alpha

    # create key for b
    Kb = Ka ^ deltaKab

    # calculate the value of Xb (semi encrypted through rounds 1-3)
    # calculate the value of Yb (semi encrypted through rounds 1-4)
    # also calculate the 7 round encryption Cb
    Xb, Yb, Cb = nmKASUMI.sandwichEnc(Pb, Kb)

    #################################################################################################################
    # Shift Ca and Cb by delta to create Cc and Cd
    Cc = Ca ^ delta

    Cd = Cb ^ delta

    #################################################################################################################
    # create keys for Cc and Cd
    Kc = Ka ^ deltaKac

    Kd = Kc ^ deltaKab

    #################################################################################################################
    # Decrypt Cc and Cd both fully and partially creating Pc, Pd, Yc, Yd and Xc, Xd

    Yc, Xc, Pc = nmKASUMI.sandwichDec(Cc, Kc)
    Yd, Xd, Pd = nmKASUMI.sandwichDec(Cd, Kd)

    #################################################################################################################
    # check conditions for right quartet-ness
    quartet = [0, 0, 0]

    # condition 1: Xa xor Xb == beta == Xc xor Xd
    if ((Xa ^ Xb) == beta) and ((Xc ^ Xd) == beta):
        print('step 1 match')
        quartet[0] = 1
    else:
        print('step 1 fail')
        # continue

    #  condition 2: Ya xor Yc == gamma
    if (Ya ^ Yc == gamma) and (Yb ^ Yd == gamma):
        print('step 2 match')
        quartet[1] = 1
    else:
        print('step 2 fail')
        # continue

    # condition 3: Ca xor Cc == delta == Cb xor Cd
    if (Ca ^ Cc == delta) and (Cb ^ Cd == delta):
        print('step 3 match')
        quartet[2] = 1
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
        print('Ka: ', hex(Ka))
        check = (Pc ^ Pd) == alpha
        if check:
            break