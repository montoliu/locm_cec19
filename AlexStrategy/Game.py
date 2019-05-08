import Agent as ag

if __name__ == '__main__':
    agent = ag.Agent()
    while True:
        agent.read_input()
        agent.act()
