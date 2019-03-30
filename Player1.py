# This agent select always the first card on the draft phase
# In the battle phase selects randomly the next action to do
import sys
import random


# ------------------------------------------------------------
# Player information
# ------------------------------------------------------------
class Player:
    def __init__(self, hp, mana, cards_remaining, rune, draw):
        self.hp = hp
        self.mana = mana
        self.cards_remaining = cards_remaining  # the number of cards in the player's deck
        self.rune = rune  # the next remaining rune of a player
        self.draw = draw  # the additional number of drawn cards


# ------------------------------------------------------------
# Card information
# ------------------------------------------------------------
class Card:
    def __init__(self, card_id, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change,
                 opponent_health_change, card_draw, lane):
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

    def has_charge(self):
        return 'C' in self.abilities


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
        self.l_cards_on_player_hand = []  # list of cards on player hand
        self.l_cards_on_left_lane_player = []  # list of cards on the left side of the player board
        self.l_cards_on_left_lane_opponent = []  # list of cards on the left side of the opponent board
        self.l_cards_on_right_lane_player = []  # list of cards on the right side of the player board
        self.l_cards_on_right_lane_opponent = []  # list of cards on the right side of the opponent board

        if not self.is_draft_phase():
            self.classify_cards()
            self.get_all_valid_action()

            print("l_cards_on_player_hand: " + str(len(self.l_cards_on_player_hand)), file=sys.stderr)
            print("l_cards_on_left_lane_player: " + str(len(self.l_cards_on_left_lane_player)), file=sys.stderr)
            print("l_cards_on_left_lane_opponent: " + str(len(self.l_cards_on_left_lane_opponent)), file=sys.stderr)
            print("l_cards_on_right_lane_player: " + str(len(self.l_cards_on_right_lane_player)), file=sys.stderr)
            print("l_cards_on_right_lane_opponent: " + str(len(self.l_cards_on_right_lane_opponent)), file=sys.stderr)
            print("l_actions: " + str(len(self.l_actions)), file=sys.stderr)
            print(self.l_actions, file=sys.stderr)

    # TODO charge ability
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
            if c.cost <= self.player1.mana:
                # ATTACK to opponent card
                for c_left in self.l_cards_on_left_lane_opponent:
                    self.l_actions.append("ATTACK " + str(c.instance_id) + " " + str(c_left.instance_id))
                for c_right in self.l_cards_on_right_lane_opponent:
                    self.l_actions.append("ATTACK " + str(c.instance_id) + " " + str(c_right.instance_id))
                # ATTACK to opponent
                self.l_actions.append("ATTACK " + str(c.instance_id) + " -1")

        # for all cards on player right side of the board
        for c in self.l_cards_on_right_lane_player:
            if c.cost <= self.player1.mana:
                # ATTACK to opponent card
                for c_left in self.l_cards_on_left_lane_opponent:
                    self.l_actions.append("ATTACK " + str(c.instance_id) + " " + str(c_left.instance_id))
                for c_right in self.l_cards_on_right_lane_opponent:
                    self.l_actions.append("ATTACK " + str(c.instance_id) + " " + str(c_right.instance_id))
                # ATTACK to opponent
                self.l_actions.append("ATTACK " + str(c.instance_id) + " -1")

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


# ------------------------------------------------------------
# Agent
# ------------------------------------------------------------
class Agent():
    def __init__(self):
        self.state = None
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
                            int(defense), abilities, (my_health_change), int(opponent_health_change), int(card_draw),
                            int(lane))
            l_cards.append(one_card)

        player1 = Player(player_health1, player_mana1, player_deck1, player_rune1, player_draw1)
        player2 = Player(player_health2, player_mana2, player_deck2, player_rune2, player_draw2)
        self.state = State(player1, player2, opponent_hand, l_opponent_actions, l_cards)

    # ----------------------------------------------
    # Select best action to do depending on the pahse
    # ----------------------------------------------
    def act(self):
        if self.state.is_draft_phase():
            self.ia_draft()
        else:
            self.ia_battle()

    # ----------------------------------------------
    # This Agent selects always the first card (0)
    # ----------------------------------------------
    def ia_draft(self):
        print("PICK 0")

    # ----------------------------------------------
    # Randomly select the action
    # ----------------------------------------------
    def ia_battle(self):
        if len(self.state.l_actions) == 0:
            print("PASS")
        else:
            coin = random.randint(0, len(self.state.l_actions) - 1)
            print(self.state.l_actions[coin])


# -------------------------------------------------------
# Main program.
# At each turn, read input and perform an action
# -------------------------------------------------------
if __name__ == '__main__':
    agent = Agent()
    while True:
        agent.read_input()
        agent.act()
