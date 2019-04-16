import random
import copy


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

    # ----------------------------------------------
    # Return the string with player data for NN
    # ----------------------------------------------
    def data_string(self):
        data_string = str(self.hp) + ',' + str(self.mana) + ',' + str(self.cards_remaining) + ',' + str(self.rune) + ',' + str(self.draw)
        return data_string


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
        self.breakthrough = False
        self.charge = False
        self.drain = False
        self.guard = False
        self.lethal = False
        self.ward = False

        for c in abilities:
            if c == 'B':
                self.breakthrough = True
            elif c == 'C':
                self.charge = True
            elif c == 'D':
                self.drain = True
            elif c == 'G':
                self.guard = True
            elif c == 'L':
                self.lethal = True
            elif c == 'W':
                self.ward = True

    # ----------------------------------------------
    # Return the string with cards on board data for NN
    # ----------------------------------------------
    def data_string(self):
        data_string = str(self.attack) + ',' + str(self.defense)
        for c in self.abilities:
            data_string += ','
            if c != '-':
                data_string += "1"
            else:
                data_string += "0"
        return data_string


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
        self.l_cards_on_player_hand = []          # list of cards on player hand
        self.l_cards_on_left_lane_player = []     # list of cards on the left side of the player board
        self.l_cards_on_left_lane_opponent = []   # list of cards on the left side of the opponent board
        self.l_cards_on_right_lane_player = []    # list of cards on the right side of the player board
        self.l_cards_on_right_lane_opponent = []  # list of cards on the right side of the opponent board
        self.l_left_opponent_cards_guard = []     # list of cards on the right side of the opponent board
        self.l_right_opponent_cards_guard = []    # list of cards on the right side of the opponent board
        self.l_left_cards_can_attack = []
        self.l_right_cards_can_attack = []

        if not self.is_draft_phase():
            self.classify_cards()

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
                self.l_left_cards_can_attack.append(c)
            elif c.location == self.LOCATION_OPPONENT_SIDE and c.lane == self.LANE_LEFT:
                self.l_cards_on_left_lane_opponent.append(c)
                if c.guard:
                    self.l_left_opponent_cards_guard.append(c)
            elif c.location == self.LOCATION_PLAYER_SIDE and c.lane == self.LANE_RIGHT:
                self.l_cards_on_right_lane_player.append(c)
                self.l_right_cards_can_attack.append(c)
            elif c.location == self.LOCATION_OPPONENT_SIDE and c.lane == self.LANE_RIGHT:
                self.l_cards_on_right_lane_opponent.append(c)
                if c.guard:
                    self.l_right_opponent_cards_guard.append(c)

    # ---------------------------------------
    # return true is the game is in the draft phase
    def is_draft_phase(self):
        return self.player1.mana == 0

    # ----------------------------------------------
    # Return the string with state data for NN
    # ----------------------------------------------
    def string_state(self):
        all_string = self.player1.data_string() + ',' + self.player2.data_string()
        for i in range(0, 8):
            all_string += ','
            if i < len(self.l_cards_on_player_hand):
                all_string += str(self.l_cards_on_player_hand[i].card_id)
            else:
                all_string += '0'
        for i in range(0, 3):
            all_string += ','
            if i < len(self.l_cards_on_left_lane_player):
                all_string += self.l_cards_on_player_hand[i].data_string()
            else:
                all_string += '0,0,0,0,0,0,0,0'
        for i in range(0, 3):
            all_string += ','
            if i < len(self.l_cards_on_right_lane_player):
                all_string += self.l_cards_on_player_hand[i].data_string()
            else:
                all_string += '0,0,0,0,0,0,0,0'
        for i in range(0, 3):
            all_string += ','
            if i < len(self.l_cards_on_left_lane_opponent):
                all_string += self.l_cards_on_player_hand[i].data_string()
            else:
                all_string += '0,0,0,0,0,0,0,0'
        for i in range(0, 3):
            all_string += ','
            if i < len(self.l_cards_on_right_lane_opponent):
                all_string += self.l_cards_on_player_hand[i].data_string()
            else:
                all_string += '0,0,0,0,0,0,0,0'
        return all_string


class AttackCards:
    def __init__(self, state):

        self.state = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        while len(self.state.l_left_cards_can_attack) > 0:
            self.attack_left(0)
        while len(self.state.l_right_cards_can_attack) > 0:
            self.attack_right(0)

    def attack_left(self, n):
        c = self.state.l_left_cards_can_attack[n]
        if len(self.state.l_left_opponent_cards_guard) > 0:
            self.l_turn.append("ATTACK " + str(c.instance_id) + " " + str(self.state.l_left_opponent_cards_guard[0].instance_id) + ";")
            if self.state.l_left_opponent_cards_guard[0].ward:
                self.state.l_left_opponent_cards_guard[0].ward = False
            elif c.lethal:
                self.state.l_left_opponent_cards_guard[0].defense = 0
            else:
                self.state.l_left_opponent_cards_guard[0].defense -= c.attack
            c.defense -= self.state.l_left_opponent_cards_guard[0].attack
            if self.state.l_left_opponent_cards_guard[0].defense <= 0:
                self.state.l_cards_on_left_lane_opponent.remove(self.state.l_left_opponent_cards_guard[0])
                self.state.l_left_opponent_cards_guard.remove(self.state.l_left_opponent_cards_guard[0])
            if c.defense <= 0:
                self.state.l_cards_on_left_lane_player.remove(c)
        elif len(self.state.l_cards_on_left_lane_opponent) > 0:
            self.l_turn.append("ATTACK " + str(c.instance_id) + " " + str(self.state.l_cards_on_left_lane_opponent[0].instance_id) + ";")
            if self.state.l_cards_on_left_lane_opponent[0].ward:
                self.state.l_cards_on_left_lane_opponent[0].ward = False
            elif c.lethal:
                self.state.l_cards_on_left_lane_opponent[0].defense = 0
            else:
                self.state.l_cards_on_left_lane_opponent[0].defense -= c.attack
            c.defense -= self.state.l_cards_on_left_lane_opponent[0].attack
            if self.state.l_cards_on_left_lane_opponent[0].defense <= 0:
                self.state.l_cards_on_left_lane_opponent.remove(self.state.l_cards_on_left_lane_opponent[0])
            if c.defense <= 0:
                self.state.l_cards_on_left_lane_player.remove(c)
        else:
            self.l_turn.append("ATTACK " + str(c.instance_id) + " -1;")
        self.state.l_left_cards_can_attack.remove(c)

    def attack_right(self, n):
        c = self.state.l_right_cards_can_attack[n]
        if len(self.state.l_right_opponent_cards_guard) > 0:
            self.l_turn.append("ATTACK " + str(c.instance_id) + " " + str(self.state.l_right_opponent_cards_guard[0].instance_id) + ";")
            if self.state.l_right_opponent_cards_guard[0].ward:
                self.state.l_right_opponent_cards_guard[0].ward = False
            elif c.lethal:
                self.state.l_right_opponent_cards_guard[0].defense = 0
            else:
                self.state.l_right_opponent_cards_guard[0].defense -= c.attack
            c.defense -= self.state.l_right_opponent_cards_guard[0].attack
            if self.state.l_right_opponent_cards_guard[0].defense <= 0:
                self.state.l_cards_on_right_lane_opponent.remove(self.state.l_right_opponent_cards_guard[0])
                self.state.l_right_opponent_cards_guard.remove(self.state.l_right_opponent_cards_guard[0])
            if c.defense <= 0:
                self.state.l_cards_on_right_lane_player.remove(c)
        elif len(self.state.l_cards_on_right_lane_opponent) > 0:
            self.l_turn.append("ATTACK " + str(c.instance_id) + " " + str(self.state.l_cards_on_right_lane_opponent[0].instance_id) + ";")
            if self.state.l_cards_on_right_lane_opponent[0].ward:
                self.state.l_cards_on_right_lane_opponent[0].ward = False
            elif c.lethal:
                self.state.l_cards_on_right_lane_opponent[0].defense = 0
            else:
                self.state.l_cards_on_right_lane_opponent[0].defense -= c.attack
            c.defense -= self.state.l_cards_on_right_lane_opponent[0].attack
            if self.state.l_cards_on_right_lane_opponent[0].defense <= 0:
                self.state.l_cards_on_right_lane_opponent.remove(self.state.l_cards_on_right_lane_opponent[0])
            if c.defense <= 0:
                self.state.l_cards_on_right_lane_player.remove(c)
        else:
            self.l_turn.append("ATTACK " + str(c.instance_id) + " -1;")
        self.state.l_right_cards_can_attack.remove(c)


class AttackHead:
    def __init__(self, state):

        self.state = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        while len(self.state.l_left_cards_can_attack) > 0:
            self.attack_left(0)
        while len(self.state.l_right_cards_can_attack) > 0:
            self.attack_right(0)

    def attack_left(self, n):
        c = self.state.l_left_cards_can_attack[n]
        if len(self.state.l_left_opponent_cards_guard) > 0:
            self.l_turn.append("ATTACK " + str(c.instance_id) + " " + str(self.state.l_left_opponent_cards_guard[0].instance_id) + ";")
            if self.state.l_left_opponent_cards_guard[0].ward:
                self.state.l_left_opponent_cards_guard[0].ward = False
            elif c.lethal:
                self.state.l_left_opponent_cards_guard[0].defense = 0
            else:
                self.state.l_left_opponent_cards_guard[0].defense -= c.attack
            c.defense -= self.state.l_left_opponent_cards_guard[0].attack
            if self.state.l_left_opponent_cards_guard[0].defense <= 0:
                self.state.l_cards_on_left_lane_opponent.remove(self.state.l_left_opponent_cards_guard[0])
                self.state.l_left_opponent_cards_guard.remove(self.state.l_left_opponent_cards_guard[0])
            if c.defense <= 0:
                self.state.l_cards_on_left_lane_player.remove(c)
        else:
            self.l_turn.append("ATTACK " + str(c.instance_id) + " -1;")
        self.state.l_left_cards_can_attack.remove(c)

    def attack_right(self, n):
        c = self.state.l_right_cards_can_attack[n]
        if len(self.state.l_right_opponent_cards_guard) > 0:
            self.l_turn.append("ATTACK " + str(c.instance_id) + " " + str(self.state.l_right_opponent_cards_guard[0].instance_id) + ";")
            if self.state.l_right_opponent_cards_guard[0].ward:
                self.state.l_right_opponent_cards_guard[0].ward = False
            elif c.lethal:
                self.state.l_right_opponent_cards_guard[0].defense = 0
            else:
                self.state.l_right_opponent_cards_guard[0].defense -= c.attack
            c.defense -= self.state.l_right_opponent_cards_guard[0].attack
            if self.state.l_right_opponent_cards_guard[0].defense <= 0:
                self.state.l_cards_on_right_lane_opponent.remove(self.state.l_right_opponent_cards_guard[0])
                self.state.l_right_opponent_cards_guard.remove(self.state.l_right_opponent_cards_guard[0])
            if c.defense <= 0:
                self.state.l_cards_on_right_lane_player.remove(c)
        else:
            self.l_turn.append("ATTACK " + str(c.instance_id) + " -1;")
        self.state.l_right_cards_can_attack.remove(c)


class SummonBalanced:
    def __init__(self, state):

        self.state = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        l_cards_can_summon_after = []
        while len(self.state.l_cards_on_player_hand) > 0:
            c = self.state.l_cards_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_cards_on_player_hand.remove(c)
                continue
            if c.card_type == self.state.TYPE_CREATURE and len(self.state.l_cards_on_left_lane_player) >= 3 and len(self.state.l_cards_on_right_lane_player) >= 3:
                l_cards_can_summon_after.append(c)
                continue
            elif c.card_type == self.state.TYPE_CREATURE:
                self.summon(c)
        self.state.l_cards_on_player_hand = l_cards_can_summon_after

    def summon(self,c):
        if len(self.state.l_cards_on_left_lane_player) < len(self.state.l_cards_on_right_lane_player):
            self.summon_left(c)
        elif len(self.state.l_cards_on_left_lane_player) > len(self.state.l_cards_on_right_lane_player):
            self.summon_right(c)
        else:
            r = random.randint(0, 1)
            if r == 0:
                self.summon_left(c)
            else:
                self.summon_right(c)
        self.state.player1.mana -= c.cost
        self.state.l_cards_on_player_hand.remove(c)

    def summon_right(self,c):
        self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_RIGHT) + ";")
        if c.charge:
            self.state.l_right_cards_can_attack.append(c)
        # if c.guard:
        #    self.left_cover = True
        self.state.l_cards_on_right_lane_player.append(c)

    def summon_left(self,c):
        self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_LEFT) + ";")
        if c.charge:
            self.state.l_left_cards_can_attack.append(c)
        # if c.guard:
        #    self.left_cover = True
        self.state.l_cards_on_left_lane_player.append(c)


class SummonLeft:
    def __init__(self, state):

        self.state = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        l_cards_can_summon_after = []
        while len(self.state.l_cards_on_player_hand) > 0:
            c = self.state.l_cards_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_cards_on_player_hand.remove(c)
                continue
            if c.card_type == self.state.TYPE_CREATURE and len(self.state.l_cards_on_left_lane_player) >= 3:
                l_cards_can_summon_after.append(c)
                continue
            elif c.card_type == self.state.TYPE_CREATURE:
                self.summon(c)
        self.state.l_cards_on_player_hand = l_cards_can_summon_after

    def summon(self, c):
        self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_LEFT) + ";")
        if c.charge:
            self.state.l_left_cards_can_attack.append(c)
        self.state.l_cards_on_left_lane_player.append(c)
        self.state.player1.mana -= c.cost
        self.state.l_cards_on_player_hand.remove(c)


class SummonRight:
    def __init__(self, state):

        self.state = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        l_cards_can_summon_after = []
        while len(self.state.l_cards_on_player_hand) > 0:
            c = self.state.l_cards_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_cards_on_player_hand.remove(c)
                continue
            if c.card_type == self.state.TYPE_CREATURE and len(self.state.l_cards_on_right_lane_player) >= 3:
                l_cards_can_summon_after.append(c)
                continue
            elif c.card_type == self.state.TYPE_CREATURE:
                self.summon(c)
        self.state.l_cards_on_player_hand = l_cards_can_summon_after

    def summon(self,c):
        self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_RIGHT) + ";")
        if c.charge:
            self.state.l_right_cards_can_attack.append(c)
        #if c.guard:
        #    self.left_cover = True
        self.state.l_cards_on_right_lane_player.append(c)
        self.state.player1.mana -= c.cost
        self.state.l_cards_on_player_hand.remove(c)


# ------------------------------------------------------------
# Turn information
# ------------------------------------------------------------
class Turn:
    def __init__(self, state, summon_strategy, attack_strategy):

        self.turn_state = copy.copy(state)
        self.summon_strategy = summon_strategy
        self.attack_strategy = attack_strategy
        self.l_turn = []
        self.create_turn()

    def create_turn(self):
        self.use_mana()
        self.attack()
        if len(self.turn_state.l_cards_on_player_hand) > 0:
            self.use_mana()
            self.attack()

    def use_mana(self):
        if self.summon_strategy == 1:
            summon_turn = SummonBalanced(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif self.summon_strategy == 2:
            summon_turn = SummonLeft(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif self.summon_strategy == 3:
            summon_turn = SummonRight(self.turn_state)
            self.l_turn += summon_turn.l_turn

    def attack(self):
        if self.attack_strategy == 1:
            attack_turn = AttackHead(self.turn_state)
            self.l_turn += attack_turn.l_turn
        elif self.attack_strategy == 2:
            attack_turn = AttackCards(self.turn_state)
            self.l_turn += attack_turn.l_turn


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
            one_card = Card(int(card_number), int(instance_id), int(location), int(card_type), int(cost), int(attack),
                                int(defense), abilities, (my_health_change), int(opponent_health_change), int(card_draw), int(lane))
            l_cards.append(one_card)

        player1 = Player(player_health1, player_mana1, player_deck1, player_rune1, player_draw1)
        player2 = Player(player_health2, player_mana2, player_deck2, player_rune2, player_draw2)
        self.last_state = copy.copy(self.state)
        self.state = State(player1, player2, opponent_hand, l_opponent_actions, l_cards)

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
        self.summon_strategy = random.randint(1, 3)
        self.attack_strategy = random.randint(1, 2)
        turn = Turn(self.state, self.summon_strategy, self.attack_strategy)
        if len(turn.l_turn) == 0:
            print("PASS")
        else:
            turn_string = ""
            for action in turn.l_turn:
                turn_string += action
            print(turn_string)

    # ----------------------------------------------
    # Calculate reward
    # ----------------------------------------------
    def reward(self):
        return self.state.player1.hp - self.last_state.player1.hp + self.last_state.player2.hp - self.state.player2.hp

    # ----------------------------------------------
    # Print to file the string to NN
    # ----------------------------------------------
    def print_NN(self, output_file):
        string_to_print = self.last_state.string_state() + ','
        string_to_print += self.state.string_state() + ','
        string_to_print += str(self.last_strategy) + ','
        string_to_print += str(self.reward())
        return string_to_print


if __name__ == '__main__':
    agent = Agent()
    i_turn = 1
    #NN = False

    #if NN:
    #    nn_file = open("nn_data.txt", "a")
    while True:
        agent.read_input()
        agent.act()
        # if NN and i_turn > 31:
        #         nn_str = agent.print_NN()
        #         nn_file.write(nn_str + '\n')
        #         nn_file.flush()
        i_turn += 1