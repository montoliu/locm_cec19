import Agent as ag

if __name__ == '__main__':
    agent = ag.Agent()
    i_turn = 1
    nn_file = open("nn_data.txt", "a+")

    while True:
        nn_file.write("Turno: " + str(i_turn) + "\n")
        agent.read_input()
        agent.act()
        #if i_turn > 31:
        #    agent.print_NN(nn_file)
        i_turn += 1

    nn_file.close()