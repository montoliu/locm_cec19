# genera las posibles combinaciones de agentes
# Como resultado escribe un script para su ejecución
#java -jar ./LoCM.jar -p1 "python3 Agente1.py" -p2 "python3 Agente2.py" import random

import os.path

n_times = 1000 # numero de partidas que cada agente realiza contra todos los demas
l_agents = ["RaulAgent.py", "AlexAgent.py", "ArturoAgent.py"]

output_filename = "go.sh"


if __name__ == '__main__':

    f = open(output_filename, "w")
    order = 'rm alexAgentCards.txt'
    print(order, file=f)
    order = 'rm raulAgentCards.txt'
    print(order, file=f)

    for i in range(n_times):
        for a1 in l_agents:
            for a2 in l_agents:
                if a1 != a2:
                    order = 'echo ' + a1 + '_' + a2
                    print(order, file=f)
                    order = 'java -jar ./LoCM.jar -p1 "python3 ' + a1 + '" -p2 ' + ' "python3 ' + a2 + '"'
                    print(order, file=f)
    f.close()
