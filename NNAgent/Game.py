import Agent as ag

if __name__ == '__main__':
    agent = ag.Agent()
    while True:
        agent.read_input()
        if agent.last_state is not None:
            agent.print_nn()
        agent.act()
