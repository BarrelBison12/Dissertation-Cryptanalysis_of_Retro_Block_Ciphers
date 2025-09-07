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
try: 
    with open("VerifySand.txt", 'x') as f:
        f.write("File created \n")
except FileExistsError:
    print('error file exists')

#################################################################################################################
# start the outer for loop - number of tests
for l in range(10000):
    print('l: ', l)
    # with open("VerifyRes1.txt", 'a') as f:
    #     f.write(f"Test {l}:\n")
    numRightQuartets = 0

    #################################################################################################################
    # start the inner for loop - number of quartets 
    for k in range(pow(2, 16)):

        #################################################################################################################
        # set up for PT a
        # create PT a
        Pa = secrets.token_hex(8)
        Pa = int(Pa, 16)

        # create key for a
        Ka = secrets.token_hex(16)


        # calculate the value of Xa (semi encrypted through rounds 1-3)
        # calculate the value of Ya (semi encrypted through rounds 1-4)
        # also calculate the 7 round encryption Ca
        Ka = int(Ka, 16)
        Xa, Ya, Ca = nmKASUMI.sandwichEnc(Pa, Ka)

        #################################################################################################################
        # set up for PT b
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
        # Decrypt Cc and Cd for both full and E1 creating Pc, Pd and Yc, Yd resp

        Yc, Xc, Pc = nmKASUMI.sandwichDec(Cc, Kc)
        Yd, Xd, Pd = nmKASUMI.sandwichDec(Cd, Kd)

        #################################################################################################################
        # check conditions for right quartet-ness
        quartet = [0, 0, 0]

        # condition 1: Xa xor Xb == beta == Xc xor Xd
        if ((Xa ^ Xb) == beta) and ((Xc ^ Xd) == beta):
            quartet[0] = 1
        else:
            continue

        #  condition 2: Ya xor Yc == gamma
        if (Ya ^ Yc == gamma) and (Yb ^ Yd == gamma):
            quartet[1] = 1
        else:
            continue

        # condition 3: Ca xor Cc == delta == Cb xor Cd
        if (Ca ^ Cc == delta) and (Cb ^ Cd == delta):
            quartet[2] = 1
        else:
            continue

        if quartet == [1, 1, 1]:
            check = (Pc ^ Pd) == alpha
            if check:
                # s = ["This is a right quartet: \n", 
                #      f"Pa: {hex(Pa)}\n",
                #      f"Pb: {hex(Pb)}\n",
                #      f"Pc: {hex(Pc)}\n",
                #      f"Pd: {hex(Pd)}\n"]
                # with open("VerifyRes1.txt", 'a') as f:
                #     f.writelines(s)
                numRightQuartets += 1
    
    s = ["Test finished\n",
         f"Number of right quartets: {numRightQuartets}\n"
        ]
    
    with open("VerifySand.txt", 'a') as f:
        f.writelines(s)
