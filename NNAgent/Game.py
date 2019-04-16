import Agent as ag

if __name__ == '__main__':
    agent = ag.Agent()
    i_turn = 1
    NN = True

    if NN:
        nn_file = open("nn_data.txt", "a")
    while True:
        agent.read_input()
        agent.act()
        if NN and i_turn > 31:
                nn_str = agent.print_NN()
                nn_file.write(nn_str + '\n')
                nn_file.flush()
        i_turn += 1
