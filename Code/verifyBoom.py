import secrets
import GOST

# (0, e31)
alpha = beta = 0x0000000080000000
# (0, 0)
gamma = 0x0000000000000000
# (e7, 0)
# delta = 0x0000008000000000
delta = 0x0000040000000000
# (e31, 0, e31, 0, e31, 0, e31, 0) - 256 bit key difference
deltaKab = 0x8000000000000000800000000000000080000000000000008000000000000000
# (e31, 0, 0, 0, 0, 0, 0, 0) - 256 bit key difference
deltaKac = 0x8000000000000000000000000000000000000000000000000000000000000000

# E0 consists of the first 24 rounds: 1-24
# E1 consists of the last 8 rounds: 25-32
# full consists of all 32 rounds

try: 
    with open("VerifyBoom2-8-10k.txt", 'x') as f:
        f.write("File created \n")
except FileExistsError:
    print('error file exists')

for k in range(10000):
    print('k: ', k)
    numRightQuartets = 0

    for w in range(pow(2, 8)):
        #################################################################################################################
        # set up for PT a
        # create PT a
        Pa = secrets.token_hex(8)
        Pa = int(Pa, 16)

        # create key for a
        Ka = secrets.token_hex(32)
        Ka = int(Ka, 16)

        # calculate the value of Xa (semi encrypted through rounds 1-24)
        # also calculate the 32 round encryption Ca
        # print('this is for a')
        Xa, Ca, za, beforea, aftera = GOST.BoomEnc(Pa, Ka)
        #################################################################################################################
        # set up for PT b
        Pb = Pa ^ alpha

        # create key for b
        Kb = Ka ^ deltaKab

        # calculate the value of Xb (semi encrypted through rounds 1-24)
        # also calculate the 32 round encryption Cb
        # print('this is for b')
        Xb, Cb, zb, beforeb, afterb = GOST.BoomEnc(Pb, Kb)
        
        # print('Xa: ', hex(Xa))
        # print('Xb: ', hex(Xb))
        # print('before xor: ', hex(beforea ^ beforeb))
        # print('after xor: ', hex(aftera ^ afterb))
        
        
        # print(za ^ zb == 0x8000000000000000)
        # if za ^ zb == 0x8000000000000000:
        #     print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            
        # if Xa ^ Xb == beta:
        #     print('/////////////////////////////////////////////////////////////////////////')

        #################################################################################################################
        # shift Ca and Cb by delta to create Cc and Cd
        Cc = Ca ^ delta

        Cd = Cb ^ delta

        #################################################################################################################
        # create keys for Cc and Cd
        Kc = Ka ^ deltaKac

        Kd = Kc ^ deltaKab

        #################################################################################################################
        # decrypt Cc and Cd both fully and partially creating Pc, Pd and Xc, Xd

        Xc, Pc = GOST.BoomDec(Cc, Kc)
        Xd, Pd = GOST.BoomDec(Cd, Kd)

        #################################################################################################################
        # check conditions for right quartet-ness
        # print('Pa: ', hex(Pa))
        # print('Pb: ', hex(Pb))
        # print('Pc: ', hex(Pc))
        # print('Pd: ', hex(Pd))

        # always true (i think)
        # print('Pa xor Pb == alpha: ', (Pa ^ Pb) == alpha)
        # print('Xa xor Xb == beta: ', (Xa ^ Xb) == beta)
        # print('Ka xor Kb == deltaKab: ', (Ka ^ Kb) == deltaKab)
        # print('Ka xor Kc == deltaKac: ', (Ka ^ Kc) == deltaKac)
        # print('Kc xor Kd == deltaKac: ', (Kc ^ Kd) == deltaKab)
        # print('Ca xor Cc == delta: ', (Ca ^ Cc) == delta)
        # print('Cb xor Cd == delta: ', (Cb ^ Cd) == delta)

        # # idk yet
        # print('Pc xor Pd == alpha: ', (Pc ^ Pd) == alpha)
        # print('Xc xor Xd == beta: ', (Xc ^ Xd) == beta)
        # print('Xa xor Xc == gamma: ', (Xa ^ Xc) == gamma)
        
        # Xpc, Cpc = GOST.BoomEnc(Pc, Kc)
        # Xpd, Cpd = GOST.BoomEnc(Pd, Kd)
        # print('Xpc == Xc: ', Xpc == Xc)
        # print('Xpd == Xd: ', Xpd == Xd)

        # start = 0xfedcba0987654321
        # startKey = 0x1111222233334444555566667777888899990000aaaabbbbccccddddeeeeffff
        # CaTest = GOST.semiE(start, startKey)
        # CcTest = CaTest ^ delta
        # CcTestKey = startKey ^ deltaKac
        # end = GOST.semiD(CcTest, CcTestKey)

        
        # print('start: ', hex(start))
        # print('end: ', hex(end))
        
        # start = secrets.token_hex(8)
        # startKey = secrets.token_hex(32)
        # start = int(start, 16)
        # startKey = int(startKey, 16)
        # CcTestKey = startKey ^ deltaKac
        
        # startDiff = start ^ delta
        # midA = GOST.semiD(start, startKey)
        # midC = GOST.semiD(startDiff, CcTestKey)
        # print('midA: ', hex(midA))
        # print('midC: ', hex(midC))
        # if midC ^ midA == gamma:
        #     break
        
        # catest2 = GOST.semiE(start, startKey)
        # cctest2 = GOST.semiE(start, CcTestKey)
        # print('catest2: ', hex(catest2))
        # print('cctest2: ', hex(cctest2))
        # print('test2 xor: ', catest2 ^ cctest2 == delta)
        # print('val: ', hex(catest2 ^ cctest2))
        # val = hex(catest2 ^ cctest2)
        # if val not in diffdic:
        #     diffdic[val] = 1
        # else:
        #     diffdic[val] += 1
        # if catest2 ^ cctest2 == delta:
        #     print('it works')
        #     break


        # start = secrets.token_hex(8)
        # startKey = secrets.token_hex(32)
        # start = int(start, 16)
        # startKey = int(startKey, 16)
        # catest2 = GOST.semiE(start, startKey)
        # cctest2 = GOST.semiE(start, CcTestKey)
        # print('catest2: ', hex(catest2))
        # print('cctest2: ', hex(cctest2))
        # print('test2 xor: ', catest2 ^ cctest2 == delta)
        # print('val: ', hex(catest2 ^ cctest2))
        # if catest2 ^ cctest2 == delta:
        #     print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        #     break
        

        # xatest = GOST.semiES(start, startKey)
        # xctest = GOST.semiES(0x0987654321fedcba, CcTestKey)
        # print('xatest: ', hex(xatest))
        # print('xctest: ', hex(xctest))
        # print('test3 xor: ', hex(xatest ^ xctest))
        



        
        if (Pc ^ Pd) == alpha:
            # print('it works')
            # print(Pa, Pb, Pc, Pd)
            # print('Pa: ', hex(Pa))
            # print('Pb: ', hex(Pb))
            # print('Pc: ', hex(Pc))
            # print('Pd: ', hex(Pd))
            # print('Ka: ', hex(Ka))
            numRightQuartets += 1
            # break
    
    s = [f"Number of right quartets: {numRightQuartets}\n"]
    
    with open("VerifyBoom2-8-10k.txt", 'a') as f:
        f.writelines(s)




f.close()
