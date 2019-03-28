# genera muchas combinaciones de posibles cartas para la fase de draft
# Como resultado escribe un script para su ejecución
#java -jar ./LoCM.jar -p1 "python3 Player1.py" -p2 "python3 PLayer2.py" -d "predefinedDraftIds=1_2_3_,_3_2_1_,_2_2_2_,160_160_160,_150_151_152,_130_131_132,_7_7_7,_8_8_8,_9_9_9,_10_10_10,_11_11_11,_12_12_12,_13_13_13,_14_14_14,_15_15_15,_16_16_16,_17_17_17,_18_18_18,_19_19_19,_20_20_20,_11_11_11,_12_12_12,_13_13_13,_14_14_14,_15_15_15,_16_16_16,_17_17_17,_18_18_18,_19_19_19,_30_30_30"
import random


n_times = 1000 # numero de partidas (cada partida una combinación)
name_agent1 = "Player1.py"
name_agent2 = "Player2.py"
output_filename = "go.sh"


def get_cards_combinations():
    s = ""
    n1 = random.randint(1,160)
    n2 = random.randint(1,160)
    n3 = random.randint(1,160)
    s = s + str(n1) + "_" + str(n2) + "_" + str(n3)
    for i in range(1, 30):
        n1 = random.randint(1,160)
        n2 = random.randint(1,160)
        n3 = random.randint(1,160)
        s = s + "," + str(n1) + "_" + str(n2) + "_" + str(n3)
    return s


if __name__ == '__main__':
    for i in range(n_times):
        s_cards = get_cards_combinations()
        order = 'java -jar ./LoCM.jar -p1 "python3 ' + name_agent1 + '" -p2 ' + ' "python3 ' + name_agent2 \
                + ' " -d "predefinedDraftIds=' + s_cards + '"'
        print(order)
