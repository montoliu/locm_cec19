import random
import Card as cd
import Player as pl
import State as st


# ------------------------------------------------------------
# Agent
# ------------------------------------------------------------
class Agent:
    def __init__(self):
        self.state = None
        self.last_state = None
        self.strategy = None
        self.last_strategy = None
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
    # read the input and fill corresponfing classes
    # ------------------------------------------------------------
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
        if self.state.player1.mana is not 0:
            self.last_state = self.state
        self.state = st.State(player1, player2, opponent_hand, l_opponent_actions, l_cards)

    # ----------------------------------------------
    # Select best action to do depending on the pahse
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
        n = random.randint(0,2)
        print("PICK " + str(n))

    # ----------------------------------------------
    # IA for battle
    # ----------------------------------------------
    def ia_battle(self):
        print ("PASS")

    # ----------------------------------------------
    #Print state, laststate, reward, estrategi
    # ----------------------------------------------
    def string_state(self, state):
        all_string = state.player1.data_string() + ',' + state.player2.data_string()
        for i in range(0, 8):
            all_string += ','
            if len(state.l_cards_on_player_hand) < i:
                all_string += state.l_cards_on_player_hand[i].card_id
            else:
                all_string += '0'
        for i in range(0, 3):
            all_string += ','
            if len(state.l_cards_on_left_lane_player) < i:
                all_string += state.l_cards_on_player_hand[i].data_string()
            else:
                all_string += '00000000'
        for i in range(0, 3):
            all_string += ','
            if len(state.l_cards_on_right_lane_player) < i:
                all_string += state.l_cards_on_player_hand[i].data_string()
            else:
                all_string += '00000000'
        for i in range(0, 3):
            all_string += ','
            if len(state.l_cards_on_left_lane_opponent) < i:
                all_string += state.l_cards_on_player_hand[i].data_string()
            else:
                all_string += '00000000'
        for i in range(0, 3):
            all_string += ','
            if len(state.l_cards_on_right_lane_opponent) < i:
                all_string += state.l_cards_on_player_hand[i].data_string()
            else:
                all_string += '00000000'

    def reward(self):
        return self.state.player1.hp - self.last_state.player1.hp + self.last_state.player2.hp - self.state.player2.hp

    def print_nn(self):
        string_to_print = self.string_state(self.last_state) + ',' + self.string_state(self.state) + ',' + str(self.last_strategy) + ',' + str(self.reward())
        file = open("nn_data.txt", "a+")
        file.write(string_to_print)
