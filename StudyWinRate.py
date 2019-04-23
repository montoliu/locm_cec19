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


if __name__ == '__main__':

    alexWins = 0
    alexGames = 0
    alexErrors = 0
    arturoWins = 0
    arturoGames = 0
    arturoErrors = 0
    diegoWins = 0
    diegoGames = 0
    diegoErrors = 0

    f = open(fileResult, "r")

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
            if agents[0] == "AlexAgent.py":
                if p1 == 1:
                    alexWins += 1
                elif p1 == -1:
                    alexErrors += 1
                alexGames += 1
            elif agents[1] == "AlexAgent.py":
                if p2 == 1:
                    alexWins += 1
                elif p2 == -1:
                    alexErrors += 1
                alexGames += 1
        if "ArturoAgent.py" in agents:
            if agents[0] == "ArturoAgent.py":
                if p1 == 1:
                    arturoWins += 1
                elif p1 == -1:
                    arturoErrors += 1
                arturoGames += 1
            elif agents[1] == "ArturoAgent.py":
                if p2 == 1:
                    arturoWins += 1
                elif p2 == -1:
                    arturoErrors += 1
                arturoGames += 1
        if "DiegoAgent.py" in agents:
            if agents[0] == "DiegoAgent.py":
                if p1 == 1:
                    diegoWins += 1
                elif p1 == -1:
                    diegoErrors += 1
                diegoGames += 1
            elif agents[1] == "DiegoAgent.py":
                if p2 == 1:
                    diegoWins += 1
                elif p2 == -1:
                    diegoErrors += 1
                diegoGames += 1


    cadena = ""
    cadena += "Alex Wins: " + str(alexWins) + " Alex Errors: " + str(alexErrors) + " Alex Games: " + str(alexGames) + " WinRate: " + str((alexWins/alexGames)*100)
    print (cadena)
    cadena = ""
    cadena += "Arturo Wins: " + str(arturoWins) + " ArturoErrors: " + str(arturoErrors) + " Arturo Games: " + str(arturoGames) + " WinRate: " + str((arturoWins/arturoGames)*100)
    print (cadena)
    cadena = ""
    cadena += "Diego Wins: " + str(diegoWins) + " DiegoErrors: " + str(diegoErrors) + " Diego Games: " + str(diegoGames) + " WinRate: " + str((diegoWins/diegoGames)*100)
    print (cadena)