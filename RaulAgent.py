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

    # return True if the card has some of the following abilities, False otherwise
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

    # return the number of abilities of the card
    def get_points_abilities(self):
        n = 0
        if self.has_breakthrough():
            n += 1
        if self.has_charge():
            n += 1
        if self.has_drain():
            n += 1
        if self.has_guard():
            n += 1
        if self.has_lethal():
            n += 1
        if self.has_ward():
            n += 1
        return n


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

        # The cards will be classified in these list
        self.l_cards_on_player_hand = []         # list of cards on player hand
        self.l_cards_on_left_lane_player = []    # list of cards on the left side of the player board
        self.l_cards_on_left_lane_opponent = []  # list of cards on the left side of the opponent board
        self.l_cards_on_right_lane_player = []   # list of cards on the right side of the player board
        self.l_cards_on_right_lane_opponent = [] # list of cards on the right side of the opponent board

        if not self.is_draft_phase():
            self.classify_cards()

            # DEBUG
            # print("l_cards_on_player_hand: " + str(len(self.l_cards_on_player_hand)), file=sys.stderr)
            # print("l_cards_on_left_lane_player: " + str(len(self.l_cards_on_left_lane_player)), file=sys.stderr)
            # print("l_cards_on_left_lane_opponent: " + str(len(self.l_cards_on_left_lane_opponent)), file=sys.stderr)
            # print("l_cards_on_right_lane_player: " + str(len(self.l_cards_on_right_lane_player)), file=sys.stderr)
            # print("l_cards_on_right_lane_opponent: " + str(len(self.l_cards_on_right_lane_opponent)), file=sys.stderr)

    # ---------------------------------------
    # Classify a card in the corresponding list
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
    # Return true is the game is in the draft phase
    def is_draft_phase(self):
        return self.player1.mana == 0


# ------------------------------------------------------------
# Draft class
# ------------------------------------------------------------
class Draft:
    def __init__(self):
        self.picked_card_type = [0, 0, 0, 0, 0, 0, 0, 0]  # number of actual picked card of each type
        self.prefer_card_type = [5, 5, 5, 5, 4, 2, 2, 2]  # desired number of cards of each type
        self.TYPE_CREATURE = 0
        self.TYPE_GREEN = 1
        self.TYPE_RED = 2
        self.TYPE_BLUE = 3

    # ------------------------------------------------------------
    # Select the best card and fill the corresponging value on picked_card_type
    def pick_card(self, cards):
        best_card = self.select_bestcard(cards)
        if cards[best_card].card_type == self.TYPE_CREATURE and cards[best_card].cost < 3:
            self.picked_card_type[0] += 1
        elif cards[best_card].card_type == self.TYPE_CREATURE and cards[best_card].cost < 5:
            self.picked_card_type[1] += 1
        elif cards[best_card].card_type == self.TYPE_CREATURE and cards[best_card].cost < 7:
            self.picked_card_type[2] += 1
        elif cards[best_card].card_type == self.TYPE_CREATURE and cards[best_card].cost < 9:
            self.picked_card_type[3] += 1
        elif cards[best_card].card_type == self.TYPE_CREATURE:
            self.picked_card_type[4] += 1
        elif cards[best_card].card_type == self.TYPE_GREEN:
            self.picked_card_type[5] += 1
        elif cards[best_card].card_type == self.TYPE_RED:
            self.picked_card_type[6] += 1
        else: # TYPE_BLUE
            self.picked_card_type[7] += 1

        return best_card

    # ------------------------------------------------------------
    # Algorithm to select the best card.
    # First select the card with more abilities.
    # If all cards have the same number of abilities: random
    # It is random, but the types (on picked_card_type) with more gaps are more probables
    def select_bestcard(self, l_cards):
        l_percent = []
        for card in l_cards:
            if card.card_type == self.TYPE_CREATURE:
                if card.cost < 3:
                    p = self.prefer_card_type[0] - self.picked_card_type[0]
                elif card.cost < 5:
                    p = self.prefer_card_type[1] - self.picked_card_type[1]
                elif card.cost < 7:
                    p = self.prefer_card_type[2] - self.picked_card_type[2]
                elif card.cost < 9:
                    p = self.prefer_card_type[3] - self.picked_card_type[3]
                else:
                    p = self.prefer_card_type[4] - self.picked_card_type[4]
            elif card.card_type == self.TYPE_GREEN:
                p = self.prefer_card_type[5] - self.picked_card_type[5]
            elif card.card_type == self.TYPE_RED:
                p = self.prefer_card_type[6] - self.picked_card_type[6]
            else:
                p = self.prefer_card_type[7] - self.picked_card_type[7]

            if p < 0:
                p = 0
            l_percent.append(p)
        if np.sum(l_percent) == 0:
            n = random.randint(0,2)
        else:
            result = random.uniform(0, np.sum(l_percent))
            if result <= l_percent[0]:
                n = 0
            elif result <= (l_percent[0]+l_percent[1]):
                n = 1
            else:
                n = 2
        return n


# ------------------------------------------------------------
# Action SUMMON
# ------------------------------------------------------------
class ActionSummon:
    def __init__(self, card, lane):
        self.type = "SUMMON"
        self.card = card
        self.lane = lane

    def get_str(self):
        return "SUMMON " + str(self.card.instance_id) + " " + str(self.lane)


# ------------------------------------------------------------
# Action USE
# ------------------------------------------------------------
class ActionUse:
    def __init__(self, card, target):
        self.type = "USE"
        self.card = card
        self.target = target

    def get_str(self):
        return "USE " + str(self.card.instance_id) + " " + str(self.target)


# ------------------------------------------------------------
# Action ATTACK
# ------------------------------------------------------------
class ActionAttack:
    def __init__(self, card, target):
        self.type = "Attack"
        self.card = card
        self.target = target

    def get_str(self):
        return "ATTACK " + str(self.card.instance_id) + " " + str(self.target)


# ------------------------------------------------------------
# Turn
# ------------------------------------------------------------
class Turn:
    def __init__(self):
        self.l_actions = []
        self.l_summoned = []          # summoned cards
        self.l_has_charge_left = []   # can attack after summoned
        self.l_has_charge_right = []  # can attack after summoned
        self.LANE_LEFT = 1
        self.LANE_RIGHT = 0

    def add_action(self, action):
        self.l_actions.append(action)
        if action.type == "SUMMON":
            self.l_summoned.append(action.card)
            if action.card.has_charge():
                if action.lane == self.LANE_LEFT:
                    self.l_has_charge_left.append(action.card)
                else:
                    self.l_has_charge_right.append(action.card)

    def get_str(self):
        s = ""
        for action in self.l_actions:
            s += action.get_str() + ";"
        if s == "":
            s = "PASS"
        return s

    def print(self):
        s = self.get_str()
        print(s)

    def debug(self):
        s = self.get_str()
        print(s, file=sys.stderr)


# ------------------------------------------------------------
# Agent
# ------------------------------------------------------------
class Agent:
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
            self.ia_draft()
        else:
            self.ia_battle()

    # ----------------------------------------------
    # This Agent selects always the second card (1)
    # ----------------------------------------------
    def ia_draft(self):
        best_card_to_pick = self.draft.pick_card(self.state.l_cards)
        print("PICK " + str(best_card_to_pick))

    # ----------------------------------------------
    # Select the action
    # ----------------------------------------------
    def ia_battle(self):
        turn = Turn()
        mana = self.state.player1.mana

        # SUMMON
        turn, mana = self.ia_summon(turn, mana)
        turn.debug()

        # USE
        turn, mana = self.ia_use(turn, mana)
        turn.debug()

        # ATTACK
        turn = self.ia_attack(turn)
        turn.debug()

        turn.print()
        turn.debug()

    # ----------------------------------------------
    # IA summon
    # ----------------------------------------------
    def ia_summon(self, turn, remaining_mana):
        n_left = len(self.state.l_cards_on_left_lane_player)
        n_right = len(self.state.l_cards_on_right_lane_player)

        for card in self.state.l_cards_on_player_hand:
            if card.cost <= remaining_mana:
                if card.card_type == self.TYPE_CREATURE:
                    if n_left < 3 or n_right < 3:
                        selected_lane, n_left, n_right = self.ia_lane(n_left, n_right)
                        action = ActionSummon(card, selected_lane)
                        turn.add_action(action)
                        remaining_mana -= card.cost

        return turn, remaining_mana

    # ----------------------------------------------
    # IA Lane
    # ----------------------------------------------
    def ia_lane(self, n_left, n_right):
        if n_left <= n_right:
            n_left += 1
            return self.LANE_LEFT, n_left, n_right

        if n_left > n_right:
            n_right += 1
            return self.LANE_RIGHT, n_left, n_right

    # ----------------------------------------------
    # IA USE
    # ----------------------------------------------
    def ia_use(self, turn, remaining_mana):
        l_own_cards = self.state.l_cards_on_left_lane_player + self.state.l_cards_on_right_lane_player + turn.l_summoned
        l_opponent_cards = self.state.l_cards_on_left_lane_opponent + self.state.l_cards_on_right_lane_opponent

        for card in self.state.l_cards_on_player_hand:
            if card.cost <= remaining_mana:
                if card.card_type == self.TYPE_BLUE:
                    action = ActionUse(card, -1)
                    turn.add_action(action)
                    remaining_mana -= card.cost
                elif card.card_type == self.TYPE_GREEN:
                    selected_target = self.ia_select_player_card_to_use_on(l_own_cards)
                    if selected_target != -1:
                        action = ActionUse(card, selected_target)
                        turn.add_action(action)
                        remaining_mana -= card.cost
                elif card.card_type == self.TYPE_BLUE:
                    selected_target = self.ia_select_opponent_card_to_use_on(l_opponent_cards)
                    if selected_target != -1:
                        action = ActionUse(card, selected_target)
                        turn.add_action(action)
                        remaining_mana -= card.cost

        return turn, remaining_mana

    # ----------------------------------------------
    # ----------------------------------------------
    def ia_select_player_card_to_use_on(self, l_own_cards):
        if len(l_own_cards) == 0:
            return -1
        coin = random.randint(0,len(l_own_cards)-1)
        return l_own_cards[coin].instance_id

    # ----------------------------------------------
    # ----------------------------------------------
    def ia_select_opponent_card_to_use_on(self, l_opponent_cards):
        if len(l_opponent_cards) == 0:
            return -1
        coin = random.randint(0, len(l_opponent_cards) - 1)
        return l_opponent_cards[coin].instance_id

    # ----------------------------------------------
    # IA attack
    # ----------------------------------------------
    # Attack to first attack until is dead, then the next one. If there isn't, attack to the opponent
    def ia_attack(self, turn):
        l_can_attack_left = self.state.l_cards_on_left_lane_player + turn.l_has_charge_left
        l_can_attack_right = self.state.l_cards_on_right_lane_player + turn.l_has_charge_right

        # LEFT
        i_opponent = 0
        i_player = 0
        n_opponent_cards = len(self.state.l_cards_on_left_lane_opponent)

        while i_player < len(l_can_attack_left):
            if n_opponent_cards == 0:
                action = ActionAttack(l_can_attack_left[i_player], -1)
                turn.add_action(action)
                i_player += 1
            else:
                action = ActionAttack(l_can_attack_left[i_player], self.state.l_cards_on_left_lane_opponent[i_opponent].instance_id)
                turn.add_action(action)
                life = self.state.l_cards_on_left_lane_opponent[i_opponent].defense - l_can_attack_left[i_player].attack
                i_player += 1

                if life <= 0:
                    i_opponent += 1
                    n_opponent_cards -= 1


        # RIGHT
        i_opponent = 0
        i_player = 0
        n_opponent_cards = len(self.state.l_cards_on_right_lane_opponent)

        while i_player < len(l_can_attack_right):
            if n_opponent_cards == 0:
                action = ActionAttack(l_can_attack_right[i_player], -1)
                turn.add_action(action)
                i_player += 1
            else:
                action = ActionAttack(l_can_attack_right[i_player], self.state.l_cards_on_right_lane_opponent[i_opponent].instance_id)
                turn.add_action(action)
                life = self.state.l_cards_on_right_lane_opponent[i_opponent].defense - l_can_attack_right[i_player].attack
                i_player += 1

                if life <= 0:
                    i_opponent += 1
                    n_opponent_cards -= 1

        return turn

# ----------------------------------------------
# ----------------------------------------------
# ----------------------------------------------
# Always pick the first card
if __name__ == '__main__':
    agent = Agent()
    while True:
        agent.read_input()
        agent.act()
