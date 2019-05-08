import random
import Card as cd
import Player as pl
import State as st
import Turn as tr
import Draft as dr
import math
import sys


# ------------------------------------------------------------
# Agent
# ------------------------------------------------------------
class Agent:
    def __init__(self):
        self.state = None
        self.draft = dr.Draft()
        self.summon_strategy = 0
        self.attack_strategy = 0
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
                                int(defense), abilities, int(my_health_change), int(opponent_health_change), int(card_draw), int(lane))
            l_cards.append(one_card)

        player1 = pl.Player(player_health1, player_mana1, player_deck1, player_rune1, player_draw1)
        player2 = pl.Player(player_health2, player_mana2, player_deck2, player_rune2, player_draw2)

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
        best_card = self.draft.pick_card(self.state.l_cards)
        print("PICK " + str(best_card))

    # ----------------------------------------------
    # IA for battle
    # ----------------------------------------------
    def ia_battle(self):
        best_reward = -math.inf
        best_turn = []
        for x in range(1, 100):
            self.summon_strategy = random.randint(3, 27)
            self.attack_strategy = random.randint(1, 9)
            print("Strategies: " + str(self.summon_strategy) + " " + str(self.attack_strategy), file=sys.stderr)
            turn = tr.Turn(self.state, self.summon_strategy, self.attack_strategy)
            print("Reward: " + str(turn.reward), file=sys.stderr)
            turn_string = ""
            for action in turn.l_turn:
                turn_string += action
            print("string: " + turn_string, file=sys.stderr)
            if turn.reward > best_reward:
                best_reward = turn.reward
                best_turn = turn.l_turn
            elif turn.reward == best_reward:
                if random.randint(0, 1):
                    best_reward = turn.reward
                    best_turn = turn.l_turn

        if len(best_turn) == 0:
            print("PASS")
        else:
            turn_string = ""
            for action in best_turn:
                turn_string += action
            print(turn_string)
