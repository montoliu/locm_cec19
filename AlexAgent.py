import random
import sys
import numpy as np


# ------------------------------------------------------------
# Player information
# ------------------------------------------------------------
class Player:
    def __init__(self, hp, mana, cards_remaining, rune, draw):
        self.hp = hp
        self.mana = mana
        self.cards_remaining = cards_remaining  # the number of cards in the player's deck
        self.rune = rune                        # the next remaining rune of a player
        self.draw = draw                        # the additional number of drawn cards


# ------------------------------------------------------------
# Card information
# ------------------------------------------------------------
class Card:
    def __init__(self, card_id, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw, lane):
        self.card_id = card_id
        self.instance_id = instance_id
        self.location = location
        self.card_type = card_type
        self.cost = cost
        self.attack = attack
        self.defense = defense
        self.abilities = abilities
        self.my_health_change = my_health_change
        self.opponent_health_change = opponent_health_change
        self.card_draw = card_draw
        self.lane = lane

    def has_breakthrough(self):
        return 'B' in self.abilities

    def has_charge(self):
        return 'C' in self.abilities

    def has_drain(self):
        return 'D' in self.abilities

    def has_guard(self):
        return 'G' in self.abilities

    def has_lethal(self):
        return 'L' in self.abilities

    def has_ward(self):
        return 'W' in self.abilities


# ------------------------------------------------------------
# State information
# ------------------------------------------------------------
class State:
    def __init__(self, player1, player2, opponent_hand, l_opponent_actions, l_cards):
        self.player1 = player1
        self.player2 = player2
        self.opponent_hand = opponent_hand
        self.l_opponent_actions = l_opponent_actions
        self.l_cards = l_cards

        self.LOCATION_IN_HAND = 0
        self.LOCATION_PLAYER_SIDE = 1
        self.LOCATION_OPPONENT_SIDE = -1

        self.LANE_LEFT = 1
        self.LANE_RIGHT = 0

        self.TYPE_CREATURE = 0
        self.TYPE_GREEN = 1
        self.TYPE_RED = 2
        self.TYPE_BLUE = 3

        self.l_actions = []
        self.l_cards_on_player_hand = []         # list of cards on player hand
        self.l_cards_on_left_lane_player = []    # list of cards on the left side of the player board
        self.l_cards_on_left_lane_opponent = []  # list of cards on the left side of the opponent board
        self.l_cards_on_right_lane_player = []   # list of cards on the right side of the player board
        self.l_cards_on_right_lane_opponent = [] # list of cards on the right side of the opponent board

        if not self.is_draft_phase():
            self.classify_cards()
            self.get_all_valid_action()

            # DEBUG
            print("l_cards_on_player_hand: " + str(len(self.l_cards_on_player_hand)), file=sys.stderr)
            print("l_cards_on_left_lane_player: " + str(len(self.l_cards_on_left_lane_player)), file=sys.stderr)
            print("l_cards_on_left_lane_opponent: " + str(len(self.l_cards_on_left_lane_opponent)), file=sys.stderr)
            print("l_cards_on_right_lane_player: " + str(len(self.l_cards_on_right_lane_player)), file=sys.stderr)
            print("l_cards_on_right_lane_opponent: " + str(len(self.l_cards_on_right_lane_opponent)), file=sys.stderr)
            print("l_actions: " + str(len(self.l_actions)), file=sys.stderr)
            print(self.l_actions, file=sys.stderr)

    # ---------------------------------------
    # Classify each card in the corresponding list (only if cost <= player mana)
    # Can attack cards on the players lane (already summoned)
    # Can be summoned criatures on the hand
    # Can be used items on the hand
    def classify_cards(self):
        for c in self.l_cards:
            if c.location == self.LOCATION_IN_HAND:
                self.l_cards_on_player_hand.append(c)
            elif c.location == self.LOCATION_PLAYER_SIDE and c.lane == self.LANE_LEFT:
                self.l_cards_on_left_lane_player.append(c)
            elif c.location == self.LOCATION_OPPONENT_SIDE and c.lane == self.LANE_LEFT:
                self.l_cards_on_left_lane_opponent.append(c)
            elif c.location == self.LOCATION_PLAYER_SIDE and c.lane == self.LANE_RIGHT:
                self.l_cards_on_right_lane_player.append(c)
            elif c.location == self.LOCATION_OPPONENT_SIDE and c.lane == self.LANE_RIGHT:
                self.l_cards_on_right_lane_opponent.append(c)

    # ---------------------------------------
    # return true is the game is in the draft phase
    def is_draft_phase(self):
        return self.player1.mana == 0

    # ---------------------------------------
    #TODO hay que cambiar muchas cosas
    def get_all_valid_action(self):
        # for all cards on player hands
        for c in self.l_cards_on_player_hand:
            if c.cost <= self.player1.mana:
                if c.card_type == self.TYPE_CREATURE:
                    # SUMMON
                    if len(self.l_cards_on_left_lane_player) < 3:
                        self.l_actions.append("SUMMON " + str(c.instance_id) + " " + str(self.LANE_LEFT))
                    if len(self.l_cards_on_right_lane_player) < 3:
                        self.l_actions.append("SUMMON " + str(c.instance_id) + " " + str(self.LANE_RIGHT))
                if c.card_type == self.TYPE_BLUE:
                    # USE on player or opponent
                    self.l_actions.append("USE " + str(c.instance_id) + " -1")
                elif c.card_type == self.TYPE_GREEN:
                    # USE on player cards
                    for c_left in self.l_cards_on_left_lane_player:
                        self.l_actions.append("USE " + str(c.instance_id) + " " + str(c_left.instance_id))
                    for c_right in self.l_cards_on_right_lane_player:
                        self.l_actions.append("USE " + str(c.instance_id) + " " + str(c_right.instance_id))
                elif c.card_type == self.TYPE_RED:
                    # USE on opponent cards:
                    for c_left in self.l_cards_on_left_lane_opponent:
                        self.l_actions.append("USE " + str(c.instance_id) + " " + str(c_left.instance_id))
                    for c_right in self.l_cards_on_right_lane_opponent:
                        self.l_actions.append("USE " + str(c.instance_id) + " " + str(c_right.instance_id))

        # for all cards on player left side of the board
        for c in self.l_cards_on_left_lane_player:
            # ATTACK to opponent card
            for c_left in self.l_cards_on_left_lane_opponent:
                self.l_actions.append("ATTACK " + str(c.instance_id) + " " + str(c_left.instance_id))
            # ATTACK to opponent
            self.l_actions.append("ATTACK " + str(c.instance_id) + " -1")

        # for all cards on player right side of the board
        for c in self.l_cards_on_right_lane_player:
            # ATTACK to opponent card
            for c_right in self.l_cards_on_right_lane_opponent:
                self.l_actions.append("ATTACK " + str(c.instance_id) + " " + str(c_right.instance_id))
            # ATTACK to opponent
            self.l_actions.append("ATTACK " + str(c.instance_id) + " -1")


# ------------------------------------------------------------
# Agent
# ------------------------------------------------------------
class AgentRandom():
    def __init__(self):
        self.state = None
        self.draft = Draft()
        self.LOCATION_IN_HAND = 0
        self.LOCATION_PLAYER_SIDE = 1
        self.LOCATION_OPPONENT_SIDE = -1

        self.LANE_LEFT = 1
        self.LANE_RIGHT = 0

        self.TYPE_CREATURE = 0
        self.TYPE_GREEN = 1
        self.TYPE_RED = 2
        self.TYPE_BLUE = 3
        self.pick = -1

    def set_pick(self, n):
        self.pick = n

    # ------------------------------------------------------------
    # read the input and fill corresponfing classes
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
            one_card = Card(int(card_number), int(instance_id), int(location), int(card_type), int(cost), int(attack),
                        int(defense), abilities, (my_health_change), int(opponent_health_change), int(card_draw), int(lane))
            l_cards.append(one_card)

        player1 = Player(player_health1, player_mana1, player_deck1, player_rune1, player_draw1)
        player2 = Player(player_health2, player_mana2, player_deck2, player_rune2, player_draw2)
        self.state = State(player1, player2, opponent_hand, l_opponent_actions, l_cards)

    # ----------------------------------------------
    # Select best action to do depending on the pahse
    # ----------------------------------------------
    def act(self):
        if self.state.is_draft_phase():
            best_card = self.draft.pick_card(self.state.l_cards)
            print("PICK " + str(best_card))

        else:
            self.ia_battle()

    # ----------------------------------------------
    # This Agent selects always the second card (1)
    # ----------------------------------------------
    def ia_draft(self):
        if self.pick == -1:
            n = random.randint(0, 2)
            print("PICK " + str(n))
        else:
            print("PICK " + str(self.pick))

    # ----------------------------------------------
    # Randomly select the action
    # ----------------------------------------------
    def ia_battle(self):
        if len(self.state.l_actions) == 0:
            print("PASS")
        else:
            #TODO hay que construir la cadena con todas las acciones que se hayan elegido
            coin = random.randint(0, len(self.state.l_actions) - 1)
            print(self.state.l_actions[coin])


# ------------------------------------------------------------
# Draft class
# ------------------------------------------------------------
class Draft:
    def __init__(self):
        self.l_all_cards_picked = []
        self.picked_card_type = [0, 0, 0, 0, 0, 0, 0, 0]
        self.prefer_card_type = [5, 5, 5, 5, 4, 2, 2, 2]
        self.l_cards_values = [0.256, 0.174, 0.18, 0.213, 0.202, 0.212, 0.304, 0.161, 0.24, 0.182, 0.227, 0.174, 0.471, 0.261, 0.341, 0.244, 0.267, 0.331, 0.383, 0.296, 0.367, 0.421, 0.479, 0.173, 0.154, 0.359, 0.293, 0.177, 0.128, 0.293, 0.23, 0.202, 0.258, 0.228, 0.266, 0.233, 0.363, 0.206, 0.215, 0.226, 0.312, 0.316, 0.43, 0.381, 0.35, 0.51, 0.205, 0.247, 0.453, 0.341, 0.408, 0.267, 0.276, 0.286, 0.162, 0.217, 0.134, 0.457, 0.567, 0.358, 0.502, 0.974, 0.269, 0.308, 0.256, 0.438, 0.516, 0.426, 0.354, 0.37, 0.172, 0.383, 0.432, 0.41, 0.528, 0.504, 0.54, 0.58, 0.489, 0.711, 0.413, 0.652, 0.084, 0.241, 0.135, 0.083, 0.302, 0.142, 0.3, 0.29, 0.169, 0.265, 0.239, 0.274, 0.228, 0.291, 0.35, 0.271, 0.33, 0.26, 0.401, 0.368, 0.416, 0.451, 0.447, 0.419, 0.48, 0.323, 0.312, 0.337, 0.537, 0.448, 0.496, 0.584, 0.551, 1.0, 0.145, 0.166, 0.105, 0.131, 0.077, 0.207, 0.102, 0.299, 0.182, 0.135, 0.192, 0.376, 0.217, 0.443, 0.257, 0.352, 0.477, 0.188, 0.429, 0.06, 0.101, 0.068, 0.199, 0.07, 0.048, 0.161, 0.013, 0.169, 0.072, 0.234, 0.0, 0.147, 0.121, 0.062, 0.281, 0.257, 0.33, 0.142, 0.207, 0.393, 0.198, 0.343, 0.492, 0.293]

    def pick_card(self, cards):
        best_card = self.select_bestcard(cards)
        if cards[best_card].card_type == 0 and cards[best_card].cost < 3:
            self.picked_card_type[0] += 1
        elif cards[best_card].card_type == 0 and cards[best_card].cost < 5:
            self.picked_card_type[1] += 1
        elif cards[best_card].card_type == 0 and cards[best_card].cost < 7:
            self.picked_card_type[2] += 1
        elif cards[best_card].card_type == 0 and cards[best_card].cost < 9:
            self.picked_card_type[3] += 1
        elif cards[best_card].card_type == 0:
            self.picked_card_type[4] += 1
        elif cards[best_card].card_type == 1:
            self.picked_card_type[5] += 1
        elif cards[best_card].card_type == 2:
            self.picked_card_type[6] += 1
        else:
            self.picked_card_type[7] += 1

        print(str(self.l_cards_values[cards[0].card_id - 1]) + " " + str(self.l_cards_values[cards[1].card_id - 1]) + " " + str(self.l_cards_values[cards[2].card_id - 1]) + " " + str(best_card), file=sys.stderr)
        self.l_all_cards_picked.append(cards[best_card])
        return best_card

    def select_bestcard(self, cards):
        n = 0
        favorite = []
        for c in cards:
            if self.l_cards_values[c.card_id - 1] == 1:
                favorite.append(c)
        if len(favorite) > 0:
            r = random.randint(0, len(favorite) - 1)
            return cards.index(favorite[r])

        l_percent = []
        for c in cards:
            p = 0
            if c.card_type == 0 and c.cost < 3:
                p = (self.prefer_card_type[0] - self.picked_card_type[0]) * self.l_cards_values[c.card_id - 1]
            elif c.card_type == 0 and c.cost < 5:
                p = (self.prefer_card_type[1] - self.picked_card_type[1]) * self.l_cards_values[c.card_id - 1]
            elif c.card_type == 0 and c.cost < 7:
                p = (self.prefer_card_type[2] - self.picked_card_type[2]) * self.l_cards_values[c.card_id - 1]
            elif c.card_type == 0 and c.cost < 9:
                p = (self.prefer_card_type[3] - self.picked_card_type[3]) * self.l_cards_values[c.card_id - 1]
            elif c.card_type == 0:
                p = (self.prefer_card_type[4] - self.picked_card_type[4]) * self.l_cards_values[c.card_id - 1]
            elif c.card_type == 1:
                p = (self.prefer_card_type[5] - self.picked_card_type[5]) * self.l_cards_values[c.card_id - 1]
            elif c.card_type == 2:
                p = (self.prefer_card_type[6] - self.picked_card_type[6]) * self.l_cards_values[c.card_id - 1]
            else:
                p = (self.prefer_card_type[7] - self.picked_card_type[7]) * self.l_cards_values[c.card_id - 1]
            l_percent.append(p)
        result = random.uniform(0, np.sum(l_percent))
        if result <= l_percent[0]:
            n = 0
        elif result <= (l_percent[0]+l_percent[1]):
            n = 1
        else:
            n = 2
        print(str(l_percent[0]) + ", " + str(l_percent[1]) + ", " + str(l_percent[2]) + " = " + str(result) + " = " + str(n), file=sys.stderr)
        return n


# ----------------------------------------------
# ----------------------------------------------
# ----------------------------------------------
# Always pick the first card
if __name__ == '__main__':
    agent = AgentRandom()
    agent.set_pick(0)
    while True:
        agent.read_input()
        agent.act()
