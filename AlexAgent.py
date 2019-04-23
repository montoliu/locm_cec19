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
        self.l_guard_cards_on_player_hand = []   # list of guard cards on player hand
        self.l_objects_cards_on_player_hand = []# list of objects cards on player hand
        self.l_creatures_cards_on_player_hand = []# list of creatures cards on player hand
        self.l_cards_on_left_lane_player = []    # list of cards on the left side of the player board
        self.l_cards_on_left_lane_opponent = []  # list of cards on the left side of the opponent board
        self.l_cards_on_right_lane_player = []   # list of cards on the right side of the player board
        self.l_cards_on_right_lane_opponent = [] # list of cards on the right side of the opponent board

        self.left_cover = False
        self.right_cover = False

        self.l_turn = []
        self.l_left_cards_can_attack = []
        self.l_left_cards_can_attack_lethal = []
        self.l_left_cards_can_attack_break = []
        self.l_right_cards_can_attack = []
        self.l_right_cards_can_attack_lethal = []
        self.l_right_cards_can_attack_break = []
        self.l_cards_on_player_board = []
        self.l_cards_on_opponent_board = []
        self.l_left_opponent_cards_guard = []
        self.l_right_opponent_cards_guard = []
        self.l_left_opponent_cards_drain_lethal = []
        self.l_right_opponent_cards_drain_lethal = []


        if not self.is_draft_phase():
            self.classify_cards()

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
                if c.card_type == self.TYPE_CREATURE:
                    self.l_creatures_cards_on_player_hand.append(c)
                    if c.guard:
                        self.l_guard_cards_on_player_hand.append(c)
                else:
                    self.l_objects_cards_on_player_hand.append(c)
            elif c.location == self.LOCATION_PLAYER_SIDE and c.lane == self.LANE_LEFT:
                self.l_cards_on_left_lane_player.append(c)
                self.l_left_cards_can_attack.append(c)
                self.l_cards_on_player_board.append(c)
                if c.guard:
                    self.left_cover = True
                if c.breakthrough:
                    self.l_left_cards_can_attack_break.append(c)
                if c.lethal:
                    self.l_left_cards_can_attack_lethal.append(c)
            elif c.location == self.LOCATION_OPPONENT_SIDE and c.lane == self.LANE_LEFT:
                self.l_cards_on_left_lane_opponent.append(c)
                self.l_cards_on_opponent_board.append(c)
                if c.guard:
                    self.l_left_opponent_cards_guard.append(c)
                if c.drain or c.lethal:
                    self.l_left_opponent_cards_drain_lethal.append(c)
            elif c.location == self.LOCATION_PLAYER_SIDE and c.lane == self.LANE_RIGHT:
                self.l_cards_on_right_lane_player.append(c)
                self.l_right_cards_can_attack.append(c)
                self.l_cards_on_player_board.append(c)
                if c.guard:
                    self.right_cover = True
                if c.breakthrough:
                    self.l_right_cards_can_attack_break.append(c)
                if c.lethal:
                    self.l_right_cards_can_attack_lethal.append(c)
            elif c.location == self.LOCATION_OPPONENT_SIDE and c.lane == self.LANE_RIGHT:
                self.l_cards_on_right_lane_opponent.append(c)
                self.l_cards_on_opponent_board.append(c)
                if c.guard:
                    self.l_right_opponent_cards_guard.append(c)
                if c.drain or c.lethal:
                    self.l_right_opponent_cards_drain_lethal.append(c)

    # ---------------------------------------
    # return true is the game is in the draft phase
    def is_draft_phase(self):
        return self.player1.mana == 0

    # ---------------------------------------
    #TODO hay que cambiar muchas cosas
    def get_turn(self):
        # for all cards on player hands
        l_turn = []
        self.l_cards_on_player_hand = self.use_mana()
        self.attack()
        if len(self.l_cards_on_player_hand) > 0:
            self.use_mana()
            self.attack()

    def use_mana(self):
        if len(self.l_cards_on_player_board) < 3:
            self.l_creatures_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=False)
            self.l_objects_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=False)
            self.l_cards_on_player_hand = self.l_creatures_cards_on_player_hand + self.l_objects_cards_on_player_hand
        else:
            self.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
        l_cards_can_summon_after = []
        if self.left_cover is not True and len(self.l_cards_on_left_lane_player) < 3:
            self.cover_left()
        elif self.right_cover is not True and len(self.l_cards_on_right_lane_player) < 3:
            self.cover_right()
        for c in self.l_cards_on_player_hand:
            if c.cost > self.player1.mana:
                continue
            if c.card_type == self.TYPE_CREATURE and len(self.l_cards_on_left_lane_player) >= 3 and len(
                    self.l_cards_on_right_lane_player) >= 3:
                l_cards_can_summon_after.append(c)
                continue
            if c.card_type == self.TYPE_GREEN and len(self.l_cards_on_left_lane_player) == 0 and len(
                    self.l_cards_on_right_lane_player) == 0:
                continue
            if c.card_type == self.TYPE_RED and len(self.l_cards_on_left_lane_opponent) == 0 and len(
                    self.l_cards_on_right_lane_opponent) == 0:
                continue
            if c.card_type == self.TYPE_CREATURE:
                self.summon(c)
            elif c.card_type == self.TYPE_GREEN:
                print("UseGreen", file=sys.stderr)
                self.use_green(c)
            elif c.card_type == self.TYPE_RED:
                self.use_red(c)
                print("UseRed", file=sys.stderr)
            elif c.card_type == self.TYPE_BLUE:
                print("UseBlue", file=sys.stderr)
                self.use_blue(c)
        return l_cards_can_summon_after

    def summon(self, c):
        if len(self.l_cards_on_left_lane_player) == 3:
            self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.LANE_RIGHT) + ";")
            if c.charge:
                self.l_right_cards_can_attack.append(c)
            if c.guard:
                self.right_cover = True
            self.l_cards_on_right_lane_player.append(c)
        elif len(self.l_cards_on_right_lane_player) == 3:
            self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.LANE_LEFT) + ";")
            if c.charge:
                self.l_left_cards_can_attack.append(c)
            if c.guard:
                self.left_cover = True
            self.l_cards_on_left_lane_player.append(c)
        else:
            left_lane_per = 3 - len(self.l_cards_on_left_lane_player)
            right_lane_per = 3 - len(self.l_cards_on_right_lane_player)
            r = random.randint(0, left_lane_per + right_lane_per)
            if r < left_lane_per:
                self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.LANE_LEFT) + ";")
                if c.charge:
                    self.l_left_cards_can_attack.append(c)
                if c.guard:
                    self.left_cover = True
                self.l_cards_on_left_lane_player.append(c)
            else:
                self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.LANE_RIGHT) + ";")
                if c.charge:
                    self.l_right_cards_can_attack.append(c)
                if c.guard:
                    self.right_cover = True
                self.l_cards_on_right_lane_player.append(c)
        self.player1.mana -= c.cost
        self.l_cards_on_player_board.append(c)
        self.l_cards_on_player_hand.remove(c)
        if c in self.l_guard_cards_on_player_hand:
            self.l_guard_cards_on_player_hand.remove(c)

    def cover_left(self):
        for c in self.l_guard_cards_on_player_hand:
            if c.cost > self.player1.mana:
                continue
            else:
                self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.LANE_LEFT) + ";")
                if c.charge:
                    self.l_left_cards_can_attack.append(c)
            self.l_cards_on_left_lane_player.append(c)
            self.l_cards_on_player_board.append(c)
            self.player1.mana -= c.cost
            self.l_guard_cards_on_player_hand.remove(c)
            self.l_cards_on_player_hand.remove(c)
            self.left_cover = True
            return

    def cover_right(self):
        for c in self.l_guard_cards_on_player_hand:
            if c.cost > self.player1.mana:
                continue
            else:
                self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.LANE_RIGHT) + ";")
                if c.charge:
                    self.l_right_cards_can_attack.append(c)
            self.l_cards_on_right_lane_player.append(c)
            self.l_cards_on_player_board.append(c)
            self.player1.mana -= c.cost
            self.l_guard_cards_on_player_hand.remove(c)
            self.l_cards_on_player_hand.remove(c)
            self.right_cover = True
            return

    def use_green(self, c):
        self.l_cards_on_player_board.sort(key=lambda x: x.cost, reverse=True)
        self.l_turn.append("USE " + str(c.instance_id) + " " + str(self.l_cards_on_player_board[0].instance_id) + ";")

        self.player1.mana -= c.cost
        self.l_cards_on_player_hand.remove(c)

    def use_red(self, c):
        best_coincidences = 0
        best_coincidence_card = self.l_cards_on_opponent_board[0]
        for enemyCard in self.l_cards_on_opponent_board:
            coincidences = 0
            if enemyCard.breakthrough and c.breakthrough:
                coincidences += 1
            if enemyCard.charge and c.charge:
                coincidences += 1
            if enemyCard.drain and c.drain:
                coincidences += 1
            if enemyCard.guard and c.guard:
                coincidences += 1
            if enemyCard.lethal and c.lethal:
                coincidences += 1
            if enemyCard.ward and c.ward:
                coincidences += 1
            if coincidences > best_coincidences:
                best_coincidences = coincidences
                best_coincidence_card = enemyCard

        if best_coincidences > 0:
            self.l_turn.append("USE " + str(c.instance_id) + " " + str(best_coincidence_card.instance_id) + ";")
            best_coincidence_card.defense += c.defense
            if best_coincidence_card.defense <= 0:
                if best_coincidence_card.lane == self.LANE_LEFT:
                    self.l_cards_on_left_lane_opponent.remove(best_coincidence_card)
                    if best_coincidence_card in self.l_left_opponent_cards_guard:
                        self.l_left_opponent_cards_guard.remove(best_coincidence_card)
                    if best_coincidence_card in self.l_left_opponent_cards_drain_lethal:
                        self.l_left_opponent_cards_drain_lethal.remove(best_coincidence_card)
                else:
                    self.l_cards_on_right_lane_opponent.remove(best_coincidence_card)
                    if best_coincidence_card in self.l_right_opponent_cards_guard:
                        self.l_right_opponent_cards_guard.remove(best_coincidence_card)
                    if best_coincidence_card in self.l_right_opponent_cards_drain_lethal:
                        self.l_right_opponent_cards_drain_lethal.remove(best_coincidence_card)
                self.l_cards_on_opponent_board.remove(best_coincidence_card)

        best_difference = 100
        c_attack = self.l_cards_on_opponent_board[0]
        for enemyCard in self.l_cards_on_opponent_board:
            diference = abs(enemyCard.defense + c.defense)
            if diference == 0:
                c_attack = enemyCard
                break
            elif diference < best_difference:
                best_difference = diference
                c_attack = enemyCard
        self.l_turn.append("USE " + str(c.instance_id) + " " + str(c_attack.instance_id) + ";")
        c_attack.defense -= c.defense
        if c_attack.defense <= 0:
            if c_attack.lane == self.LANE_LEFT:
                self.l_cards_on_left_lane_opponent.remove(c_attack)
                if c_attack in self.l_left_opponent_cards_guard:
                    self.l_left_opponent_cards_guard.remove(c_attack)
                if c_attack in self.l_left_opponent_cards_drain_lethal:
                    self.l_left_opponent_cards_drain_lethal.remove(c_attack)
            else:
                self.l_cards_on_right_lane_opponent.remove(c_attack)
                if c_attack in self.l_right_opponent_cards_guard:
                    self.l_right_opponent_cards_guard.remove(c_attack)
                if best_coincidence_card in self.l_right_opponent_cards_drain_lethal:
                    self.l_right_opponent_cards_drain_lethal.remove(c_attack)
            self.l_cards_on_opponent_board.remove(c_attack)
        self.player1.mana -= c.cost
        self.l_cards_on_player_hand.remove(c)

    def use_blue(self, c):
        print("l_cards_on_player_hand: " + str(len(self.l_cards_on_player_hand)), file=sys.stderr)
        if c.defense < 0:
            best_difference = 30
            c_attack = self.l_cards_on_opponent_board[0]
            for enemyCard in self.l_cards_on_opponent_board:
                diference = abs(enemyCard.defense + c.defense)
                if diference == 0:
                    c_attack = enemyCard
                    break
                elif diference < best_difference:
                    best_difference = diference
                    c_attack = enemyCard
            self.l_turn.append("USE " + str(c.instance_id) + " " + str(c_attack.instance_id) + ";")
            c_attack.defense -= c.defense
            if c_attack.defense <= 0:
                if c_attack.lane == self.LANE_LEFT:
                    self.l_cards_on_left_lane_opponent.remove(c_attack)
                    if c_attack in self.l_left_opponent_cards_guard:
                        self.l_left_opponent_cards_guard.remove(c_attack)
                    if c_attack in self.l_left_opponent_cards_drain_lethal:
                        self.l_left_opponent_cards_drain_lethal.remove(c_attack)
                else:
                    self.l_cards_on_right_lane_opponent.remove(c_attack)
                    if c_attack in self.l_right_opponent_cards_guard:
                        self.l_right_opponent_cards_guard.remove(c_attack)
                    if c_attack in self.l_right_opponent_cards_drain_lethal:
                        self.l_right_opponent_cards_drain_lethal.remove(c_attack)
                self.l_cards_on_opponent_board.remove(c_attack)
        else:
            self.l_turn.append("USE " + str(c.instance_id) + " -1;")
        self.player1.mana -= c.cost
        self.l_cards_on_player_hand.remove(c)

    def attack(self):
        if self.possible_win():
            for c in self.l_left_cards_can_attack:
                self.l_turn.append("ATTACK " + str(c.instance_id) + " -1;")
            for c in self.l_right_cards_can_attack:
                self.l_turn.append("ATTACK " + str(c.instance_id) + " -1;")
        else:
            self.l_left_cards_can_attack.sort(key=lambda x: x.attack, reverse=True)
            while len(self.l_left_cards_can_attack) > 0:
                if len(self.l_left_cards_can_attack_lethal) > 0:
                    self.attack_left(self.l_left_cards_can_attack.index(self.l_left_cards_can_attack_lethal[0]))
                else:
                    self.attack_left(0)
            self.l_right_cards_can_attack.sort(key=lambda x: x.attack, reverse=True)
            while len(self.l_right_cards_can_attack) > 0:
                if len(self.l_right_cards_can_attack_lethal) > 0:
                    self.attack_right(self.l_right_cards_can_attack.index(self.l_right_cards_can_attack_lethal[0]))
                else:
                    self.attack_right(0)

    def possible_win(self):
        n = 0
        if len(self.l_left_opponent_cards_guard) == 0:
            for c in self.l_left_cards_can_attack:
                n += c.attack
        if len(self.l_right_opponent_cards_guard) == 0:
            for c in self.l_right_cards_can_attack:
                n += c.attack
        if n >= self.player2.hp:
            return True
        return False

    def attack_left(self, n):
        c = self.l_left_cards_can_attack[n]
        if c.attack > 0 or c.lethal == True:
            #Si tiene cartas con G atacaremos a la primera carta de ese array
            if len(self.l_left_opponent_cards_guard) > 0:
                if c.lethal is not True:
                    self.l_right_opponent_cards_guard.sort(key=lambda x: x.defense, reverse=False)
                else:
                    self.l_right_opponent_cards_guard.sort(key=lambda x: x.defense, reverse=True)                #Si la siguiente carta de
                if c.lethal is not True and len(self.l_left_cards_can_attack) > n+1 and self.l_left_cards_can_attack[n+1].attack >= self.l_left_opponent_cards_guard[0].defense:
                    self.attack_left(n+1)
                    return
                else:
                    self.l_turn.append("ATTACK " + str(c.instance_id) + " " + str(
                        self.l_left_opponent_cards_guard[0].instance_id) + ";")
                    if self.l_left_opponent_cards_guard[0].ward:
                        self.l_left_opponent_cards_guard[0].ward = False
                    elif c.lethal:
                        self.l_left_opponent_cards_guard[0].defense = 0
                    else:
                        self.l_left_opponent_cards_guard[0].defense -= c.attack
                    c.defense -= self.l_left_opponent_cards_guard[0].attack
                    if self.l_left_opponent_cards_guard[0].defense <= 0:
                        self.l_cards_on_left_lane_opponent.remove(self.l_left_opponent_cards_guard[0])
                        self.l_cards_on_opponent_board.remove(self.l_left_opponent_cards_guard[0])
                        if self.l_left_opponent_cards_guard[0].lethal or self.l_left_opponent_cards_guard[0].drain:
                            self.l_left_opponent_cards_drain_lethal.remove(self.l_left_opponent_cards_guard[0])
                        self.l_left_opponent_cards_guard.remove(self.l_left_opponent_cards_guard[0])
                    if c.defense <= 0:
                        self.l_cards_on_left_lane_player.remove(c)
                        self.l_cards_on_player_board.remove(c)
            elif len(self.l_left_opponent_cards_drain_lethal) > 0:
                if c.lethal is not True:
                    self.l_left_opponent_cards_drain_lethal.sort(key=lambda x: x.defense, reverse=False)
                else:
                    self.l_left_opponent_cards_drain_lethal.sort(key=lambda x: x.defense, reverse=True)
                if c.lethal is not True and len(self.l_left_cards_can_attack) > n+1 and self.l_left_cards_can_attack[n + 1].attack >= self.l_left_opponent_cards_drain_lethal[0].defense:
                    self.attack_left(n + 1)
                    return
                else:
                    self.l_turn.append("ATTACK " + str(c.instance_id) + " " + str(
                        self.l_left_opponent_cards_drain_lethal[0].instance_id) + ";")
                    if self.l_left_opponent_cards_drain_lethal[0].ward:
                        self.l_left_opponent_cards_drain_lethal[0].ward = False
                    elif c.lethal:
                        self.l_left_opponent_cards_drain_lethal[0].defense = 0
                    else:
                        self.l_left_opponent_cards_drain_lethal[0].defense -= c.attack
                    c.defense -= self.l_left_opponent_cards_drain_lethal[0].attack
                    if self.l_left_opponent_cards_drain_lethal[0].defense <= 0:
                        self.l_cards_on_opponent_board.remove(self.l_left_opponent_cards_drain_lethal[0])
                        self.l_cards_on_left_lane_opponent.remove(self.l_left_opponent_cards_drain_lethal[0])
                        self.l_left_opponent_cards_drain_lethal.remove(self.l_left_opponent_cards_drain_lethal[0])
                    if c.defense <= 0:
                        self.l_cards_on_left_lane_player.remove(c)
                        self.l_cards_on_player_board.remove(c)
            else:
                self.l_turn.append("ATTACK " + str(c.instance_id) + " -1;")
        if c in self.l_left_cards_can_attack_lethal:
            self.l_left_cards_can_attack_lethal.remove(c)
        self.l_left_cards_can_attack.remove(c)

    def attack_right(self, n):
        c = self.l_right_cards_can_attack[n]
        if c.attack > 0 or c.lethal == True:
            # Si tiene cartas con G atacaremos a la primera carta de ese array
            if len(self.l_right_opponent_cards_guard) > 0:
                if c.lethal is not True:
                    self.l_right_opponent_cards_guard.sort(key=lambda x: x.defense, reverse=False)
                else:
                    self.l_right_opponent_cards_guard.sort(key=lambda x: x.defense, reverse=True)
                # Si la siguiente carta de
                if c.lethal is not True and len(self.l_right_cards_can_attack) > n+1 and self.l_right_cards_can_attack[n + 1].attack >= self.l_right_opponent_cards_guard[0].defense:
                    self.attack_right(n + 1)
                    return
                else:
                    self.l_turn.append("ATTACK " + str(c.instance_id) + " " + str(
                        self.l_right_opponent_cards_guard[0].instance_id) + ";")
                    if self.l_right_opponent_cards_guard[0].ward:
                        self.l_right_opponent_cards_guard[0].ward = False
                    elif c.lethal:
                        self.l_right_opponent_cards_guard[0].defense = 0
                    else:
                        self.l_right_opponent_cards_guard[0].defense -= c.attack
                    c.defense -= self.l_right_opponent_cards_guard[0].attack
                    if self.l_right_opponent_cards_guard[0].defense <= 0:
                        self.l_cards_on_right_lane_opponent.remove(self.l_right_opponent_cards_guard[0])
                        self.l_cards_on_opponent_board.remove(self.l_right_opponent_cards_guard[0])
                        if self.l_right_opponent_cards_guard[0].lethal or self.l_right_opponent_cards_guard[0].drain:
                            self.l_right_opponent_cards_drain_lethal.remove(self.l_right_opponent_cards_guard[0])
                        self.l_right_opponent_cards_guard.remove(self.l_right_opponent_cards_guard[0])
                    if c.defense <= 0:
                        self.l_cards_on_right_lane_player.remove(c)
                        self.l_cards_on_player_board.remove(c)
            elif len(self.l_right_opponent_cards_drain_lethal) > 0:
                if c.lethal is not True:
                    self.l_right_opponent_cards_drain_lethal.sort(key=lambda x: x.defense, reverse=False)
                else:
                    self.l_right_opponent_cards_drain_lethal.sort(key=lambda x: x.defense, reverse=True)
                if c.lethal is not True and len(self.l_right_cards_can_attack) > n+1 and self.l_right_cards_can_attack[n + 1].attack >= self.l_right_opponent_cards_drain_lethal[0].defense:
                    self.attack_right(n + 1)
                    return
                else:
                    self.l_turn.append("ATTACK " + str(c.instance_id) + " " + str(
                        self.l_right_opponent_cards_drain_lethal[0].instance_id) + ";")
                    if self.l_right_opponent_cards_drain_lethal[0].ward:
                        self.l_right_opponent_cards_drain_lethal[0].ward = False
                    elif c.lethal:
                        self.l_right_opponent_cards_drain_lethal[0].defense = 0
                    else:
                        self.l_right_opponent_cards_drain_lethal[0].defense -= c.attack
                    c.defense -= self.l_right_opponent_cards_drain_lethal[0].attack
                    if self.l_right_opponent_cards_drain_lethal[0].defense <= 0:
                        self.l_cards_on_opponent_board.remove(self.l_right_opponent_cards_drain_lethal[0])
                        self.l_cards_on_right_lane_opponent.remove(self.l_right_opponent_cards_drain_lethal[0])
                        self.l_right_opponent_cards_drain_lethal.remove(self.l_right_opponent_cards_drain_lethal[0])
                    if c.defense <= 0:
                        self.l_cards_on_right_lane_player.remove(c)
                        self.l_cards_on_player_board.remove(c)
            else:
                self.l_turn.append("ATTACK " + str(c.instance_id) + " -1;")
        if c in self.l_right_cards_can_attack_lethal:
            self.l_right_cards_can_attack_lethal.remove(c)
        self.l_right_cards_can_attack.remove(c)


# ------------------------------------------------------------
# Agent
# ------------------------------------------------------------
class AgentRandom:
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
                        int(defense), abilities, int(my_health_change), int(opponent_health_change), int(card_draw), int(lane))

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
            turn_string = ""
            for action in self.state.l_turn:
                turn_string += action
            print(turn_string)


# ------------------------------------------------------------
# Draft class
# ------------------------------------------------------------
class Draft:
    def __init__(self):
        self.l_all_cards_picked = [0] * 160
        self.cards_picket = 0
        self.picked_card_type = [0, 0, 0, 0, 0, 0, 0, 0]
        self.prefer_card_type = [8, 9, 6, 4, 1, 1, 1]
        self.picked_card_guard = 0
        self.prefer_guard_card = 10
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
        elif cards[best_card].card_type == self.TYPE_CREATURE:
            self.picked_card_type[3] += 1
        elif cards[best_card].card_type == self.TYPE_GREEN:
            self.picked_card_type[4] += 1
        elif cards[best_card].card_type == self.TYPE_RED:
            self.picked_card_type[5] += 1
        else:  # TYPE_BLUE
            self.picked_card_type[6] += 1
        if cards[best_card].guard:
            self.picked_card_guard += 1
        self.l_all_cards_picked[cards[best_card].card_id - 1] += 1
        self.cards_picket += 1
        if self.cards_picket == 30:
            file = open("alexAgentCards.txt", "a")
            data = ''
            for c in self.l_all_cards_picked:
                data += str(c)
            file.write(data + '\n')
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
                else:
                    p = self.prefer_card_type[3] - self.picked_card_type[3]
            elif card.card_type == self.TYPE_GREEN:
                p = self.prefer_card_type[4] - self.picked_card_type[4]
            elif card.card_type == self.TYPE_RED:
                p = self.prefer_card_type[5] - self.picked_card_type[5]
            else:
                p = self.prefer_card_type[6] - self.picked_card_type[6]
            if card.guard:
                p += (self.prefer_guard_card - self.picked_card_guard)/2

            if p < 0:
                p = 0
            l_percent.append(p)
        if np.sum(l_percent) == 0:
            n = random.randint(0, 2)
        else:
            result = random.uniform(0, np.sum(l_percent))
            if result <= l_percent[0]:
                n = 0
            elif result <= (l_percent[0] + l_percent[1]):
                n = 1
            else:
                n = 2
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
