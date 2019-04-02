#0
#1
#shufflePlayer0Seed=-2810075176897610214
#seed=-2645199096425364235
#draftChoicesSeed=-2420534940217140885
#shufflePlayer1Seed=6313007743108444311
#predefinedDraftIds=150_2_120,39_66_139,77_157_24,42_57_51,91_118_17,5_129_81,91_136_155,29_90_97,65_16_13,145_67_61,94_88_111,157_64_97,103_80_135,78_122_30,126_79_63,147_128_124,68_102_67,118_104_26,5_5_10,61_4_79,101_6_107,97_119_4,155_58_55,143_1_57,30_132_113,85_21_72,138_103_139,56_117_74,143_74_142,55_102_130
#
import numpy as np

filename = "res.txt"

if __name__ == '__main__':

    cards_points = np.zeros(160)
    cards_times = np.zeros(160)

    f = open(filename,"r")

    # line 1: points player 1. 1 won, 0 lose
    # line 2,3,4,5,6 are not interesting
    # line 7: predefinedDraftIds
    # line 8: empty

    while True:
        p1 = f.readline()
        if not p1:
            break
        p1 = int(p1)
        f.readline()
        f.readline()
        f.readline()
        f.readline()
        f.readline()

        s = f.readline()
        f.readline()

        line = s.split(sep="=")
        cards = line[1].split(sep=",")
        for c in cards:
            l = c.split("_")
            if p1 == 1:
                cards_points[int(l[0])-1] += 1
                cards_points[int(l[1])-1] -= 1
            else:
                cards_points[int(l[0])-1] -= 1
                cards_points[int(l[1])-1] += 1
            cards_times[int(l[0]) - 1] += 1
            cards_times[int(l[1]) - 1] += 1
    f.close()

    for i in range(160):
        if cards_times[i] != 0:
            cards_points[i] = (cards_points[i] / cards_times[i])*100
    print(cards_times)
    print(cards_points)

    print (np.max(cards_points))
    print (np.argmax(cards_points))

    print (np.min(cards_points))
    print (np.argmin(cards_points))
