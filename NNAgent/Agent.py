import random
import copy
import Card as cd
import Player as pl
import State as st
import Turn as tr

# ------------------------------------------------------------
# Agent
# ------------------------------------------------------------
class Agent:
    def __init__(self):
        self.state = None
        self.last_state = None
        self.strategy = 0
        self.last_strategy = 0
        self.summon_strategy = 0
        self.last_summon_strategy = 0
        self.attack_strategy = 0
        self.last_attack_strategy = 0
        self.LOCATION_IN_HAND = 0
        self.LOCATION_PLAYER_SIDE = 1
        self.LOCATION_OPPONENT_SIDE = -1

        self.LANE_LEFT = 1
        self.LANE_RIGHT = 0

        self.TYPE_CREATURE = 0
        self.TYPE_GREEN = 1
        self.TYPE_RED = 2
        self.TYPE_BLUE = 3

    # ------------------------------------------------------------
    # Read the input
    # ------------------------------------------------------------
    def read_input(self):
        player_health1, player_mana1, player_deck1, player_rune1, player_draw1 = [int(j) for j in input().split()]
        player_health2, player_mana2, player_deck2, player_rune2, player_draw2 = [int(j) for j in input().split()]

        opponent_hand, opponent_actions = [int(i) for i in input().split()]
        l_opponent_actions = []
        for i in range(opponent_actions):
            card_number_and_action = input()
            l_opponent_actions.append(card_number_and_action)

        card_count = int(input())
        l_cards = []
        for i in range(card_count):
            card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw, lane = input().split()
            one_card = cd.Card(int(card_number), int(instance_id), int(location), int(card_type), int(cost), int(attack),
                                int(defense), abilities, (my_health_change), int(opponent_health_change), int(card_draw), int(lane))
            l_cards.append(one_card)

        player1 = pl.Player(player_health1, player_mana1, player_deck1, player_rune1, player_draw1)
        player2 = pl.Player(player_health2, player_mana2, player_deck2, player_rune2, player_draw2)
        self.last_state = copy.copy(self.state)
        self.state = st.State(player1, player2, opponent_hand, l_opponent_actions, l_cards)

    # ----------------------------------------------
    # Select best action to do depending on the phase
    # ----------------------------------------------
    def act(self):
        if self.state.is_draft_phase():
            self.ia_draft()
        else:
            self.ia_battle()

    # ----------------------------------------------
    # IA for pick
    # ----------------------------------------------
    def ia_draft(self):
        n = random.randint(0, 2)
        print("PICK " + str(n))

    # ----------------------------------------------
    # IA for battle
    # ----------------------------------------------
    def ia_battle(self):
        self.summon_strategy = 2
        self.attack_strategy = 0
        turn = tr.Turn(self.state, self.summon_strategy, self.attack_strategy)
        if len(turn.l_turn) == 0:
            print("PASS")
        else:
            turn_string = ""
            for action in turn.l_turn:
                turn_string += action
            print(turn_string)

    # ----------------------------------------------
    #Calculate reward
    # ----------------------------------------------
    def reward(self):
        return self.state.player1.hp - self.last_state.player1.hp + self.last_state.player2.hp - self.state.player2.hp

    # ----------------------------------------------
    # Print to file the string to NN
    # ----------------------------------------------
    def print_NN(self):
        string_to_print = self.last_state.string_state() + ','
        string_to_print += self.state.string_state() + ','
        string_to_print += str(self.last_strategy) + ','
        string_to_print += str(self.reward())
        return string_to_print
