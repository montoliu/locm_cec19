#Agent1.py Agent2.py
#0
#1
#shufflePlayer0Seed=-2810075176897610214
#seed=-2645199096425364235
#draftChoicesSeed=-2420534940217140885
#shufflePlayer1Seed=6313007743108444311
#predefinedDraftIds=150_2_120,39_66_139,77_157_24,42_57_51,91_118_17,5_129_81,91_136_155,29_90_97,65_16_13,145_67_61,94_88_111,157_64_97,103_80_135,78_122_30,126_79_63,147_128_124,68_102_67,118_104_26,5_5_10,61_4_79,101_6_107,97_119_4,155_58_55,143_1_57,30_132_113,85_21_72,138_103_139,56_117_74,143_74_142,55_102_130
#
import numpy as np

fileResult = "result.txt"
fileRaul = "raulAgentCards.txt"
fileAlex = "alexAgentCards.txt"


if __name__ == '__main__':

    cards_points = np.zeros(160)
    cards_times = np.zeros(160)

    f = open(fileResult, "r")
    fr = open(fileRaul, "r")
    fa = open(fileAlex, "r")

    # line 1: points player 1. 1 won, 0 lose
    # line 2,3,4,5,6 are not interesting
    # line 7: predefinedDraftIds
    # line 8: empty

    while True:

        agents = f.readline()
        print (agents)
        if not agents:
            break
        agents = agents.split(sep="_")

        p1 = f.readline()
        print (p1)
        if not p1:
            break
        p1 = int(p1)
        p2 = f.readline()
        print (p2)
        if not p2:
            break
        p2 = int(p2)
        f.readline()
        f.readline()
        f.readline()
        f.readline()
        f.readline()

        if "AlexAgent.py" in agents:
            cards = fa.readline()
            cards = list(cards)
            if agents[0] == "AlexAgent.py":
                for i in range(len(cards)-1):
                    if p1 == 1:
                        cards_points[i] += int(cards[i])
                    else:
                        cards_points[i] -= int(cards[i])
                    cards_times[i] += int(cards[i])
            elif agents[1] == "AlexAgent.py":
                for i in range(len(cards)):
                    if p1 == 1:
                        cards_points[i] -= int(cards[i])
                    else:
                        cards_points[i] += int(cards[i])
                    cards_times[i] += int(cards[i])
        if "RaulAgent.py" in agents:
            cards = fr.readline()
            cards = list(cards)
            if agents[0] == "RaulAgent.py":
                for i in range(len(cards)-1):
                    if p1 == 1:
                        cards_points[i] += int(cards[i])
                    else:
                        cards_points[i] -= int(cards[i])
                    cards_times[i] += int(cards[i])
            elif agents[1] == "RaulAgent.py":
                for i in range(len(cards)):
                    if p1 == 1:
                        cards_points[i] -= int(cards[i])
                    else:
                        cards_points[i] += int(cards[i])
                    cards_times[i] += int(cards[i])
    f.close()
    fa.close()
    fr.close()
    for i in range(160):
        if cards_times[i] != 0:
            cards_points[i] = (cards_points[i] / cards_times[i])*100
    print(cards_points)
    print(np.min(cards_points))
    print(np.max(cards_points))

    cards_points = (cards_points - np.min(cards_points)) / (np.max(cards_points)-np.min(cards_points))
    print(cards_points)
    cadena = ""
    for i in range(160):
        cadena += str(round(cards_points[i], 3)) + ", "
    print (cadena)
