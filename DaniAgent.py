import random
import sys
import numpy as np


#-------------------------------------------
# File loader and saver
ATTACKS = "Dani/DaniAttacks.txt"
ALLY = "Dani/DaniAlly.txt"
ENEMY = "Dani/DaniUsesEnemy.txt"
CHOOSES = "Dani/DaniChooses.txt"


def loadTable(fileName):

    dicti = {}
    file= open(fileName, mode='r')
    for line in file:
        splitted = line.split('|')
        a= int(splitted[0])
        b= int(splitted[1])
        c= float(splitted[2])
        dicti[(a,b)]=c
    file.close()
    return dicti

def saveTable(fileName, dicti):
    old = loadTable(fileName)
    file = open(fileName, mode='w')
    for i in old:
        a = i[0]
        b= i[1]
        c = dicti[i]+old[i]
        line = str(a)+"|"+str(b)+"|"+str(c)+"\n"
        file.write(line)
    file.close()

def loadArray(fileName):
    dicti = {}
    file = open(fileName, mode='r')
    for line in file:
        array = line.split('|')
        a = int(array[0])
        c = float(array[1])
        dicti[a] = c
    file.close()
    return dicti


def saveArray(fileName, dicti):
    old = loadArray(fileName)
    file = open(fileName, mode='w')
    for i in dicti:
        a = i
        c = dicti[i]+old[i]
        line = str(a)+"|"+str(c)+"\n"
        file.write(line)
    file.close()

tableAttacks = loadTable(ATTACKS)
tableAlly = loadTable(ALLY)
tableUsesEnemy = loadTable(ENEMY)
arrayChooses = loadArray(CHOOSES)
resultAttacks = {}
resultAlly = {}
resultUsesEnemy = {}
resultChooses = {}
taken = []
for i in range(1,161):
    for j in range(-1, 161):
        resultAttacks[(i,j)] = 0
        resultAlly[(i,j)] = 0
        resultUsesEnemy[(i,j)] = 0
for i in range(1,161):
    resultChooses[i] = 0


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
        self.breakthrough = False
        self.charge = False
        self.drain = False
        self.guard = False
        self.lethal = False
        self.ward = False
        for c in abilities:
            if c == 'B': self.breakthrough = True
            elif c == 'C': self.charge = True
            elif c == 'D':self.drain = True
            elif c == 'G': self.guard = True
            elif c == 'L': self.lethal = True
            elif c == 'W': self.ward = True






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

        self.TARGET_HEAD = player1
        self.TARGET_ENEMY = player2

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

        self.l_turn = []
        self.l_cards_can_attack = []
        self.l_cards_on_player_board = []
        self.l_cards_on_opponent_board = []
        self.l_left_opponent_cards_guard = []
        self.l_right_opponent_cards_guard = []

        self.end = False

        if not self.is_draft_phase():
            self.classify_cards()
    """
            # DEBUG
            print("l_cards_on_player_hand: " + str(len(self.l_cards_on_player_hand)), file=sys.stderr)
            print("l_cards_on_left_lane_player: " + str(len(self.l_cards_on_left_lane_player)), file=sys.stderr)
            print("l_cards_on_left_lane_opponent: " + str(len(self.l_cards_on_left_lane_opponent)), file=sys.stderr)
            print("l_cards_on_right_lane_player: " + str(len(self.l_cards_on_right_lane_player)), file=sys.stderr)
            print("l_cards_on_right_lane_opponent: " + str(len(self.l_cards_on_right_lane_opponent)), file=sys.stderr)
            print("l_actions: " + str(len(self.l_actions)), file=sys.stderr)
            print(self.l_actions, file=sys.stderr)
    """
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
                self.l_cards_can_attack.append(c)
                self.l_cards_on_player_board.append(c)
            elif c.location == self.LOCATION_OPPONENT_SIDE and c.lane == self.LANE_LEFT:
                self.l_cards_on_left_lane_opponent.append(c)
                self.l_cards_on_opponent_board.append(c)
                if c.guard:
                    self.l_left_opponent_cards_guard.append(c)
            elif c.location == self.LOCATION_PLAYER_SIDE and c.lane == self.LANE_RIGHT:
                self.l_cards_on_right_lane_player.append(c)
                self.l_cards_can_attack.append(c)
                self.l_cards_on_player_board.append(c)
            elif c.location == self.LOCATION_OPPONENT_SIDE and c.lane == self.LANE_RIGHT:
                self.l_cards_on_right_lane_opponent.append(c)
                self.l_cards_on_opponent_board.append(c)
                if c.guard:
                    self.l_right_opponent_cards_guard.append(c)

    # ---------------------------------------
    # return true is the game is in the draft phase
    def is_draft_phase(self):
        return self.player1.mana == 0


        ###########
        # ACTIONS #
        ###########

    def actionSummon(self, card: Card, lane):
        self.l_turn.append("SUMMON " + str(card.instance_id) + " " + str(lane) + ";")
        if card.charge:
            self.l_cards_can_attack.append(card)
        self.player1.mana -= card.cost
        self.l_cards_on_player_hand.remove(card)
        self.player2.hp += card.opponent_health_change

    def actionUse(self, card: Card, to):
        if to == self.TARGET_ENEMY:
            self.l_turn.append("USE " + str(card.instance_id) + " -1;")
            self.player2.hp -= card.attack
        else:
            self.l_turn.append("USE " + str(card.instance_id) + " " + str(to.instance_id) + ";")
        self.player1.mana -= card.cost
        self.l_cards_on_player_hand.remove(card)
        self.player2.hp += card.opponent_health_change
        if card.card_id == 157:
            self.player2.hp -= 1

    def actionAttack(self, card: Card, to):
        if to == self.TARGET_ENEMY:
            self.l_turn.append("ATTACK " + str(card.instance_id) + " -1;")
            to.hp -= card.attack

        else:
            self.l_turn.append("ATTACK " + str(card.instance_id) + " " + str(to.instance_id) + ";")
                                                                                                                        #TODO: Resvisar desde aquí....
            if to.ward:
                to.ward = False
            elif card.lethal:
                to.defense = 0
            elif card.breakthrough:
                if to.defense < card.attack:
                    self.player2.hp-=card.attack-to.defense
                to.defense -= card.attack
            else:
                to.defense -= card.attack

            if card.ward:
                card.ward = False
            elif to.lethal:
                card.defense = 0
            elif to.drain:
                if card.defense < card.attack:
                    self.player2.hp += card.defense
                else:
                    self.player2.hp += to.attack
                to.defense -= card.attack
            else:
                card.defense -= to.attack
                                                                                                                        #TODO: ... hasta aquí de que siempre sea cierto
            self.killIfDead(to)
            self.killIfDead(card)
        self.l_cards_can_attack.remove(card)


    def killIfDead(self, card: Card):
        if card.defense <= 0:
            lane = card.lane
            side = card.location
            if lane == self.LANE_LEFT and side == self.LOCATION_OPPONENT_SIDE :
                self.l_cards_on_left_lane_opponent.remove(card)
                if card in self.l_left_opponent_cards_guard:
                    self.l_left_opponent_cards_guard.remove(card)
                self.l_cards_on_opponent_board.remove(card)
            elif lane == self.LANE_RIGHT and side == self.LOCATION_OPPONENT_SIDE :
                self.l_cards_on_right_lane_opponent.remove(card)
                if card in self.l_right_opponent_cards_guard:
                    self.l_right_opponent_cards_guard.remove(card)
                self.l_cards_on_opponent_board.remove(card)
            elif lane == self.LANE_LEFT and side == self.LOCATION_PLAYER_SIDE :
                self.l_cards_on_left_lane_player.remove(card)
                self.l_cards_on_player_board.remove(card)
            elif lane == self.LANE_LEFT and side == self.LOCATION_PLAYER_SIDE :
                self.l_cards_on_right_lane_player.remove(card)
                self.l_cards_on_player_board.remove(card)

    def victory(self):
        if not self.end:
            saveArray(CHOOSES,resultChooses)
            self.end=True




    # ---------------------------------------
    #TODO hay que cambiar muchas cosas
    def get_turn(self):
        # for all cards on player hands
        l_turn = []
        self.l_cards_on_player_hand = self.summon()
        self.attack()
        if len(self.l_cards_on_player_hand) > 0:
             self.summon()
             self.attack()


    def summon(self):
        self.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
        l_cards_can_summon_after = []
        for c in self.l_cards_on_player_hand:
            if c.cost > self.player1.mana:
                continue
            if c.card_type == self.TYPE_CREATURE and len(self.l_cards_on_left_lane_player) >= 3 and len(self.l_cards_on_left_lane_player) >= 3:
                l_cards_can_summon_after.append(c)
                continue
            if c.card_type == self.TYPE_GREEN and len(self.l_cards_on_left_lane_player) == 0 and len(self.l_cards_on_right_lane_player) == 0:
                l_cards_can_summon_after.append(c)
                continue
            if c.card_type == self.TYPE_RED and len(self.l_cards_on_left_lane_opponent) == 0 and len(self.l_cards_on_right_lane_opponent) == 0:
                continue
            if c.card_type == self.TYPE_CREATURE:
                if len(self.l_cards_on_left_lane_player) == 3 and len(self.l_cards_on_right_lane_player) == 3:
                    l_cards_can_summon_after.append(c)
                elif len(self.l_cards_on_left_lane_player) == 3:
                    self.actionSummon(c, self.LANE_RIGHT)

                elif len(self.l_cards_on_right_lane_player) == 3:
                    self.actionSummon(c, self.LANE_LEFT)
                else:
                    left_lane_per = 3 - len(self.l_cards_on_left_lane_player)
                    right_lane_per = 3 - len(self.l_cards_on_right_lane_player)
                    r = random.randint(0, left_lane_per + right_lane_per -1)
                    if r < left_lane_per:
                        self.actionSummon(c, self.LANE_LEFT)
                    else:
                        self.actionSummon(c, self.LANE_RIGHT)

            elif c.card_type == self.TYPE_GREEN:
                r = random.randint(0,  len(self.l_cards_on_player_board) - 1)
                self.actionUse(c, self.l_cards_on_player_board[r])
            elif c.card_type == self.TYPE_RED:
                r = random.randint(0, len(self.l_cards_on_opponent_board)-1)
                self.actionUse(c, self.l_cards_on_opponent_board[r])
                self.l_cards_on_opponent_board[r].defense -= c.defense
                self.killIfDead(self.l_cards_on_opponent_board[r])
            elif c.card_type == self.TYPE_BLUE:
                if c.defense < 0:
                    r = random.randint(-1, len(self.l_cards_on_opponent_board) - 1)
                    if r < 0:
                        self.actionUse(c, self.TARGET_ENEMY)
                        self.player2.hp -= c.attack
                    else:
                        self.actionUse(c, self.l_cards_on_opponent_board[r])
                        self.l_cards_on_opponent_board[r].defense -= c.defense
                        self.killIfDead(self.l_cards_on_opponent_board[r])
                else:
                    self.actionUse(c, self.TARGET_ENEMY)
            if self.player2.hp<=0:
                self.victory()
        return l_cards_can_summon_after

    def attack(self):

        for c in self.l_cards_can_attack:

            if c.lane == self.LANE_LEFT:
                if len(self.l_left_opponent_cards_guard) > 0:
                    if not c.ward or not c.guard:
                        r = random.randint(0, len(self.l_left_opponent_cards_guard)-1)
                        self.actionAttack(c, self.l_left_opponent_cards_guard[r])
                else:
                    if not c.ward or not c.guard:
                        r = random.randint(-1, len(self.l_cards_on_left_lane_opponent)-1)
                        if r < 0:
                            self.actionAttack(c, self.TARGET_ENEMY)
                        else:
                            self.actionAttack(c, self.l_cards_on_left_lane_opponent[r])
                    else:
                        self.actionAttack(c, self.TARGET_ENEMY)
            elif c.lane == self.LANE_RIGHT:
                if len(self.l_right_opponent_cards_guard) > 0:
                    if not c.ward or not c.guard:
                        r = random.randint(0, len(self.l_right_opponent_cards_guard)-1)
                        self.actionAttack(c, self.l_right_opponent_cards_guard[r])
                else:
                    if not c.ward or not c.guard:
                        r = random.randint(-1, len(self.l_cards_on_right_lane_opponent) - 1)
                        if r < 0:
                            self.actionAttack(c, self.TARGET_ENEMY)
                        else:
                            self.actionAttack(c, self.l_cards_on_right_lane_opponent[r])
                    else:
                        self.actionAttack(c, self.TARGET_ENEMY)
            if self.player2.hp <= 0:
                self.victory()




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

        self.turn = []

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
    # Select best action to do depending on the phase
    # ----------------------------------------------
    def act(self):
        if self.state.is_draft_phase():
            best_card = self.draft.pick_card(self.state.l_cards)
            resultChooses[self.state.l_cards[best_card].card_id]+=0.02

            print("PICK " + str(best_card))

        else:
            self.turn = self.state.get_turn()
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
        if len(self.state.l_turn) == 0:
            print("PASS")
        else:
            #TODO hay que construir la cadena con todas las acciones que se hayan elegido
            turn_string = ""
            for action in self.state.l_turn:
                turn_string += action
            #coin = random.randint(0, len(self.state.l_actions) - 1)
            print(turn_string)


# ------------------------------------------------------------
# Draft class
# ------------------------------------------------------------
class Draft:
    def __init__(self):
        self.l_all_cards_picked = []
        self.picked_card_type = [0, 0, 0, 0, 0, 0, 0, 0]
        self.prefer_card_type = [5, 5, 5, 5, 4, 2, 2, 2]
        #self.l_cards_values = [0.256, 0.174, 0.18, 0.213, 0.202, 0.212, 0.304, 0.161, 0.24, 0.182, 0.227, 0.174, 0.471, 0.261, 0.341, 0.244, 0.267, 0.331, 0.383, 0.296, 0.367, 0.421, 0.479, 0.173, 0.154, 0.359, 0.293, 0.177, 0.128, 0.293, 0.23, 0.202, 0.258, 0.228, 0.266, 0.233, 0.363, 0.206, 0.215, 0.226, 0.312, 0.316, 0.43, 0.381, 0.35, 0.51, 0.205, 0.247, 0.453, 0.341, 0.408, 0.267, 0.276, 0.286, 0.162, 0.217, 0.134, 0.457, 0.567, 0.358, 0.502, 0.974, 0.269, 0.308, 0.256, 0.438, 0.516, 0.426, 0.354, 0.37, 0.172, 0.383, 0.432, 0.41, 0.528, 0.504, 0.54, 0.58, 0.489, 0.711, 0.413, 0.652, 0.084, 0.241, 0.135, 0.083, 0.302, 0.142, 0.3, 0.29, 0.169, 0.265, 0.239, 0.274, 0.228, 0.291, 0.35, 0.271, 0.33, 0.26, 0.401, 0.368, 0.416, 0.451, 0.447, 0.419, 0.48, 0.323, 0.312, 0.337, 0.537, 0.448, 0.496, 0.584, 0.551, 1.0, 0.145, 0.166, 0.105, 0.131, 0.077, 0.207, 0.102, 0.299, 0.182, 0.135, 0.192, 0.376, 0.217, 0.443, 0.257, 0.352, 0.477, 0.188, 0.429, 0.06, 0.101, 0.068, 0.199, 0.07, 0.048, 0.161, 0.013, 0.169, 0.072, 0.234, 0.0, 0.147, 0.121, 0.062, 0.281, 0.257, 0.33, 0.142, 0.207, 0.393, 0.198, 0.343, 0.492, 0.293]

    def pick_card(self, cards):
        a = arrayChooses[cards[0].card_id]
        b = arrayChooses[cards[1].card_id]
        c = arrayChooses[cards[2].card_id]
        minn = min(a,b,c)
        a = a - minn+1
        b = b - minn+1
        c = c - minn+1
        vala = a
        valb = a+b
        valc = a+b+c
        num = random.random() * valc
        if num < vala:

            return 0
        if num < valb:
            return 1
        return 2




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
