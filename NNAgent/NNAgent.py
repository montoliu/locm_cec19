import random
import copy
import numpy as np


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
        self.use_mana(self.summon_strategy)
        self.attack()
        if len(self.turn_state.l_cards_on_player_hand) + len(self.turn_state.l_green_objects_on_player_hand) + len(
                self.turn_state.l_blue_objects_on_player_hand) + len(self.turn_state.l_red_objects_on_player_hand) > 0:
            self.use_mana(self.summon_strategy)
            self.attack()

    def use_mana(self, strategy):
        if strategy == 1:
            # Summon two lanes balanced
            summon_turn = SummonBalanced(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif strategy == 2:
            # Summon only left
            summon_turn = SummonLeft(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif strategy == 3:
            # Summon only right
            summon_turn = SummonRight(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif strategy == 4:
            # Summon trying cover two lanes with guard and after summon two lanes balanced
            # summon_turn = scb.SummonCoverOrBalanced(self.turn_state)
            summon_turn = CoverLanes(self.turn_state)
            self.l_turn += summon_turn.l_turn
            self.use_mana(1)
        elif strategy == 5:
            # Summon trying cover two lanes with guard and after summon only left
            # summon_turn = scl.SummonCoverOrLeft(self.turn_state)
            summon_turn = CoverLanes(self.turn_state)
            self.l_turn += summon_turn.l_turn
            self.use_mana(2)
        elif strategy == 6:
            # Summon trying cover two lanes with guard and after summon only right
            # summon_turn = scr.SummonCoverOrRight(self.turn_state)
            summon_turn = CoverLanes(self.turn_state)
            self.l_turn += summon_turn.l_turn
            self.use_mana(3)
        elif strategy == 7:
            # Summon two lanes balanced with cost <
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=False)
            self.use_mana(1)
        elif strategy == 8:
            # Summon two lanes balanced with cost >
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
            self.use_mana(1)
        elif strategy == 9:
            # Summon only left with cost <
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=False)
            self.use_mana(2)
        elif strategy == 10:
            # Summon only left with cost >
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
            self.use_mana(2)
        elif strategy == 11:
            # Summon only right with cost <
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=False)
            self.use_mana(3)
        elif strategy == 12:
            # Summon only right with cost >
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
            self.use_mana(3)
        elif strategy == 13:
            # Summon trying cover two lanes with guard and after summon two lanes balanced with cost <
            # summon_turn = scb.SummonCoverOrBalanced(self.turn_state)
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=False)
            self.turn_state.l_guard_creatures_on_player_hand.sort(key=lambda x: x.cost, reverse=False)
            self.use_mana(4)
        elif strategy == 14:
            # Summon trying cover two lanes with guard and after summon two lanes balanced with cost >
            # summon_turn = scb.SummonCoverOrBalanced(self.turn_state)
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
            self.turn_state.l_guard_creatures_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
            self.use_mana(4)
        elif strategy == 15:
            # Summon trying cover two lanes with guard and after summon only left with cost <
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=False)
            self.turn_state.l_guard_creatures_on_player_hand.sort(key=lambda x: x.cost, reverse=False)
            self.use_mana(5)
        elif strategy == 16:
            # Summon trying cover two lanes with guard and after summon only left with cost >
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
            self.turn_state.l_guard_creatures_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
            self.use_mana(5)
        elif strategy == 17:
            # Summon trying cover two lanes with guard and after summon only right with cost <
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=False)
            self.turn_state.l_guard_creatures_on_player_hand.sort(key=lambda x: x.cost, reverse=False)
            self.use_mana(6)
        elif strategy == 18:
            # Summon trying cover two lanes with guard and after summon only right with cost >
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
            self.turn_state.l_guard_creatures_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
            self.use_mana(6)
        elif strategy == 19:
            # Only use green objects
            summon_turn = UseGreen(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif strategy == 20:
            # Only use red objects
            summon_turn = UseRed(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif strategy == 21:
            # Only use blue objects
            summon_turn = UseBlue(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif strategy == 22:
            # Only use green and red objects
            self.use_mana(19)
            self.use_mana(20)
        elif strategy == 23:
            # Only use green and blue objects
            self.use_mana(19)
            self.use_mana(21)
        elif strategy == 24:
            # Only use red and green objects
            self.use_mana(20)
            self.use_mana(19)
        elif strategy == 25:
            # Only use blue and green objects
            self.use_mana(21)
            self.use_mana(19)
        elif strategy == 26:
            # Only use blue and red objects
            self.use_mana(21)
            self.use_mana(20)
        elif strategy == 27:
            # Only use red and blue objects
            self.use_mana(20)
            self.use_mana(21)
        elif strategy == 28:
            # Only use green, red and blue objects
            self.use_mana(19)
            self.use_mana(27)
        elif strategy == 29:
            # Only use green, blue and red objects
            self.use_mana(19)
            self.use_mana(26)
        elif strategy == 30:
            # Only use red, green and blue objects
            self.use_mana(20)
            self.use_mana(23)
        elif strategy == 31:
            # Only use red, blue and green objects
            self.use_mana(20)
            self.use_mana(25)
        elif strategy == 32:
            # Only use blue, green and red objects
            self.use_mana(21)
            self.use_mana(22)
        elif strategy == 33:
            # Only use blue, red and green objects
            self.use_mana(21)
            self.use_mana(24)
        elif strategy == 33:
            # Summon left and after summon right
            self.use_mana(2)
            self.use_mana(3)
        elif strategy == 33:
            # Summon right and after summon left
            self.use_mana(3)
            self.use_mana(2)
        elif strategy == 33:
            # use abjects G-R-B and cover/balanced cost <
            self.use_mana(28)
            self.use_mana(7)

    def attack(self):
        if self.attack_strategy == 1:
            attack_turn = AttackHead(self.turn_state)
            self.l_turn += attack_turn.l_turn
        elif self.attack_strategy == 2:
            attack_turn = AttackCards(self.turn_state)
            self.l_turn += attack_turn.l_turn


# ------------------------------------------------------------
# Draft class
# ------------------------------------------------------------
class Draft:
    def __init__(self):
        self.picked_card_type = [0, 0, 0, 0, 0, 0, 0, 0]
        self.prefer_card_type = [9, 10, 7, 4, 0, 0, 0]
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


# ------------------------------------------------------------
# Summon strategies class
# ------------------------------------------------------------
# ------------------------------------------------------------
# Cover two lanes with guard
# ------------------------------------------------------------
class CoverLanes:
    def __init__(self, state):

        self.state = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        if self.state.left_cover is not True and len(self.state.l_cards_on_left_lane_player) < 3:
            self.cover_left()
        if self.state.right_cover is not True and len(self.state.l_cards_on_right_lane_player) < 3:
            self.cover_right()
        return self.l_turn

    def cover_left(self):
        while len(self.state.l_guard_creatures_on_player_hand) > 0:
            c = self.state.l_guard_creatures_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_guard_creatures_on_player_hand.remove(c)
                continue
            else:
                self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_LEFT) + ";")
                if c.charge:
                    self.state.l_left_cards_can_attack.append(c)
            self.state.l_cards_on_left_lane_player.append(c)
            self.state.player1.mana -= c.cost
            self.state.l_guard_creatures_on_player_hand.remove(c)
            self.state.l_cards_on_player_hand.remove(c)
            self.state.left_cover = True
            return

    def cover_right(self):
        while len(self.state.l_guard_creatures_on_player_hand) > 0:
            c = self.state.l_guard_creatures_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_guard_creatures_on_player_hand.remove(c)
                continue
            else:
                self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_RIGHT) + ";")
                if c.charge:
                    self.state.l_right_cards_can_attack.append(c)
            self.state.l_cards_on_right_lane_player.append(c)
            self.state.player1.mana -= c.cost
            self.state.l_guard_creatures_on_player_hand.remove(c)
            self.state.l_cards_on_player_hand.remove(c)
            self.state.right_cover = True
            return


# ------------------------------------------------------------
# Summon all left
# ------------------------------------------------------------
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
                self.state.l_cards_on_player_hand.remove(c)
                continue
            elif c.card_type == self.state.TYPE_CREATURE:
                self.summon(c)
            else:
                self.state.l_cards_on_player_hand.remove(c)
        self.state.l_cards_on_player_hand = l_cards_can_summon_after

    def summon(self, c):
        self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_LEFT) + ";")
        if c.charge:
            self.state.l_left_cards_can_attack.append(c)
        self.state.l_cards_on_left_lane_player.append(c)
        self.state.player1.mana -= c.cost
        self.state.l_cards_on_player_hand.remove(c)


# ------------------------------------------------------------
# Summon all right
# ------------------------------------------------------------
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
                self.state.l_cards_on_player_hand.remove(c)
                continue
            elif c.card_type == self.state.TYPE_CREATURE:
                self.summon(c)
            else:
                self.state.l_cards_on_player_hand.remove(c)
        self.state.l_cards_on_player_hand = l_cards_can_summon_after

    def summon(self, c):
        self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_RIGHT) + ";")
        if c.charge:
            self.state.l_right_cards_can_attack.append(c)
        # if c.guard:
        #    self.left_cover = True
        self.state.l_cards_on_right_lane_player.append(c)
        self.state.player1.mana -= c.cost
        self.state.l_cards_on_player_hand.remove(c)


# ------------------------------------------------------------
# Summon balanced
# ------------------------------------------------------------
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
            if c.card_type == self.state.TYPE_CREATURE and len(self.state.l_cards_on_left_lane_player) >= 3 and len(
                    self.state.l_cards_on_right_lane_player) >= 3:
                l_cards_can_summon_after.append(c)
                self.state.l_cards_on_player_hand.remove(c)
                continue
            elif c.card_type == self.state.TYPE_CREATURE:
                self.summon(c)
            else:
                self.state.l_cards_on_player_hand.remove(c)
        self.state.l_cards_on_player_hand = l_cards_can_summon_after

    def summon(self, c):
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

    def summon_right(self, c):
        self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_RIGHT) + ";")
        if c.charge:
            self.state.l_right_cards_can_attack.append(c)
        # if c.guard:
        #    self.left_cover = True
        self.state.l_cards_on_right_lane_player.append(c)

    def summon_left(self, c):
        self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_LEFT) + ";")
        if c.charge:
            self.state.l_left_cards_can_attack.append(c)
        # if c.guard:
        #    self.left_cover = True
        self.state.l_cards_on_left_lane_player.append(c)


# ------------------------------------------------------------
# Summon all balanced trying cover two lanes with guard
# ------------------------------------------------------------
class SummonCoverOrBalanced:
    def __init__(self, state):

        self.state = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        if self.state.left_cover is not True and len(self.state.l_cards_on_left_lane_player) < 3:
            self.cover_left()
        if self.state.right_cover is not True and len(self.state.l_cards_on_right_lane_player) < 3:
            self.cover_right()
        l_cards_can_summon_after = []
        while len(self.state.l_cards_on_player_hand) > 0:
            c = self.state.l_cards_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_cards_on_player_hand.remove(c)
                continue
            if c.card_type == self.state.TYPE_CREATURE and len(self.state.l_cards_on_left_lane_player) >= 3 and len(
                    self.state.l_cards_on_right_lane_player) >= 3:
                l_cards_can_summon_after.append(c)
                self.state.l_cards_on_player_hand.remove(c)
                continue
            elif c.card_type == self.state.TYPE_CREATURE:
                self.summon(c)
            else:
                self.state.l_cards_on_player_hand.remove(c)
        self.state.l_cards_on_player_hand = l_cards_can_summon_after

    def summon(self, c):
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

    def summon_right(self, c):
        self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_RIGHT) + ";")
        if c.charge:
            self.state.l_right_cards_can_attack.append(c)
        # if c.guard:
        #    self.left_cover = True
        self.state.l_cards_on_right_lane_player.append(c)

    def summon_left(self, c):
        self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_LEFT) + ";")
        if c.charge:
            self.state.l_left_cards_can_attack.append(c)
        # if c.guard:
        #    self.left_cover = True
        self.state.l_cards_on_left_lane_player.append(c)

    def cover_left(self):
        while len(self.state.l_guard_creatures_on_player_hand) > 0:
            c = self.state.l_guard_creatures_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_guard_creatures_on_player_hand.remove(c)
                continue
            else:
                self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_LEFT) + ";")
                if c.charge:
                    self.state.l_left_cards_can_attack.append(c)
            self.state.l_cards_on_left_lane_player.append(c)
            self.state.player1.mana -= c.cost
            self.state.l_guard_creatures_on_player_hand.remove(c)
            self.state.l_cards_on_player_hand.remove(c)
            self.state.left_cover = True
            return

    def cover_right(self):
        while len(self.state.l_guard_creatures_on_player_hand) > 0:
            c = self.state.l_guard_creatures_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_guard_creatures_on_player_hand.remove(c)
                continue
            else:
                self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_RIGHT) + ";")
                if c.charge:
                    self.state.l_right_cards_can_attack.append(c)
            self.state.l_cards_on_right_lane_player.append(c)
            self.state.player1.mana -= c.cost
            self.state.l_guard_creatures_on_player_hand.remove(c)
            self.state.l_cards_on_player_hand.remove(c)
            self.state.right_cover = True
            return


# ------------------------------------------------------------
# Summon all left trying cover two lanes with guard
# ------------------------------------------------------------
class SummonCoverOrLeft:
    def __init__(self, state):

        self.state = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        if self.state.left_cover is not True and len(self.state.l_cards_on_left_lane_player) < 3:
            self.cover_left()
        if self.state.right_cover is not True and len(self.state.l_cards_on_right_lane_player) < 3:
            self.cover_right()
        l_cards_can_summon_after = []
        while len(self.state.l_cards_on_player_hand) > 0:
            c = self.state.l_cards_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_cards_on_player_hand.remove(c)
                continue
            if c.card_type == self.state.TYPE_CREATURE and len(self.state.l_cards_on_left_lane_player) >= 3:
                l_cards_can_summon_after.append(c)
                self.state.l_cards_on_player_hand.remove(c)
                continue
            elif c.card_type == self.state.TYPE_CREATURE:
                self.summon(c)
            else:
                self.state.l_cards_on_player_hand.remove(c)
        self.state.l_cards_on_player_hand = l_cards_can_summon_after

    def summon(self, c):
        self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_LEFT) + ";")
        if c.charge:
            self.state.l_left_cards_can_attack.append(c)
        self.state.l_cards_on_left_lane_player.append(c)
        self.state.player1.mana -= c.cost
        self.state.l_cards_on_player_hand.remove(c)

    def cover_left(self):
        while len(self.state.l_guard_creatures_on_player_hand) > 0:
            c = self.state.l_guard_creatures_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_guard_creatures_on_player_hand.remove(c)
                continue
            else:
                self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_LEFT) + ";")
                if c.charge:
                    self.state.l_left_cards_can_attack.append(c)
            self.state.l_cards_on_left_lane_player.append(c)
            self.state.player1.mana -= c.cost
            self.state.l_guard_creatures_on_player_hand.remove(c)
            self.state.l_cards_on_player_hand.remove(c)
            self.state.left_cover = True
            return

    def cover_right(self):
        while len(self.state.l_guard_creatures_on_player_hand) > 0:
            c = self.state.l_guard_creatures_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_guard_creatures_on_player_hand.remove(c)
                continue
            else:
                self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_RIGHT) + ";")
                if c.charge:
                    self.state.l_right_cards_can_attack.append(c)
            self.state.l_cards_on_right_lane_player.append(c)
            self.state.player1.mana -= c.cost
            self.state.l_guard_creatures_on_player_hand.remove(c)
            self.state.l_cards_on_player_hand.remove(c)
            self.state.right_cover = True
            return


# ------------------------------------------------------------
# Summon all Right trying cover two lanes with guard
# ------------------------------------------------------------
class SummonCoverOrRight:
    def __init__(self, state):

        self.state = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        if self.state.left_cover is not True and len(self.state.l_cards_on_left_lane_player) < 3:
            self.cover_left()
        if self.state.right_cover is not True and len(self.state.l_cards_on_right_lane_player) < 3:
            self.cover_right()
        l_cards_can_summon_after = []
        while len(self.state.l_cards_on_player_hand) > 0:
            c = self.state.l_cards_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_cards_on_player_hand.remove(c)
                continue
            if c.card_type == self.state.TYPE_CREATURE and len(self.state.l_cards_on_right_lane_player) >= 3:
                l_cards_can_summon_after.append(c)
                self.state.l_cards_on_player_hand.remove(c)
                continue
            elif c.card_type == self.state.TYPE_CREATURE:
                self.summon(c)
            else:
                self.state.l_cards_on_player_hand.remove(c)
        self.state.l_cards_on_player_hand = l_cards_can_summon_after

    def summon(self, c):
        self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_RIGHT) + ";")
        if c.charge:
            self.state.l_right_cards_can_attack.append(c)
        # if c.guard:
        #    self.left_cover = True
        self.state.l_cards_on_right_lane_player.append(c)
        self.state.player1.mana -= c.cost
        self.state.l_cards_on_player_hand.remove(c)

    def cover_left(self):
        while len(self.state.l_guard_creatures_on_player_hand) > 0:
            c = self.state.l_guard_creatures_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_guard_creatures_on_player_hand.remove(c)
                continue
            else:
                self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_LEFT) + ";")
                if c.charge:
                    self.state.l_left_cards_can_attack.append(c)
            self.state.l_cards_on_left_lane_player.append(c)
            self.state.player1.mana -= c.cost
            self.state.l_guard_creatures_on_player_hand.remove(c)
            self.state.l_cards_on_player_hand.remove(c)
            self.state.left_cover = True
            return

    def cover_right(self):
        while len(self.state.l_guard_creatures_on_player_hand) > 0:
            c = self.state.l_guard_creatures_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_guard_creatures_on_player_hand.remove(c)
                continue
            else:
                self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_RIGHT) + ";")
                if c.charge:
                    self.state.l_right_cards_can_attack.append(c)
            self.state.l_cards_on_right_lane_player.append(c)
            self.state.player1.mana -= c.cost
            self.state.l_guard_creatures_on_player_hand.remove(c)
            self.state.l_cards_on_player_hand.remove(c)
            self.state.right_cover = True
            return


# ------------------------------------------------------------
# Use green objects
# ------------------------------------------------------------
class UseBlue:
    def __init__(self, state):

        self.state = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        l_cards_can_summon_after = []
        while len(self.state.l_blue_objects_on_player_hand) > 0:
            c = self.state.l_blue_objects_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_blue_objects_on_player_hand.remove(c)
                continue
            else:
                self.use(c)
        self.state.l_blue_objects_on_player_hand = l_cards_can_summon_after

    def use(self, c):
        if c.defense < 0 and len(self.state.l_cards_on_opponent_board) > 0:
            best_difference = 30
            c_attack = self.state.l_cards_on_opponent_board[0]
            for enemyCard in self.state.l_cards_on_opponent_board:
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
                if c_attack.lane == self.state.LANE_LEFT:
                    self.state.l_cards_on_left_lane_opponent.remove(c_attack)
                    if c_attack in self.state.l_left_opponent_cards_guard:
                        self.state.l_left_opponent_cards_guard.remove(c_attack)
                else:
                    self.state.l_cards_on_right_lane_opponent.remove(c_attack)
                    if c_attack in self.state.l_right_opponent_cards_guard:
                        self.state.l_right_opponent_cards_guard.remove(c_attack)
                self.state.l_cards_on_opponent_board.remove(c_attack)
        else:
            self.l_turn.append("USE " + str(c.instance_id) + " -1;")
        self.state.player1.mana -= c.cost
        self.state.l_blue_objects_on_player_hand.remove(c)
        self.state.l_cards_on_player_hand.remove(c)


# ------------------------------------------------------------
# Use green objects
# ------------------------------------------------------------
class UseGreen:
    def __init__(self, state):

        self.state = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        l_cards_can_summon_after = []
        while len(self.state.l_green_objects_on_player_hand) > 0:
            c = self.state.l_green_objects_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_cards_on_player_hand.remove(c)
                continue
            if len(self.state.l_cards_on_player_board) == 0:
                l_cards_can_summon_after.append(c)
                self.state.l_green_objects_on_player_hand.remove(c)
                continue
            else:
                self.use(c)
        self.state.l_green_objects_on_player_hand = l_cards_can_summon_after

    def use(self, c):
        self.state.l_cards_on_player_board.sort(key=lambda x: x.cost, reverse=True)
        self.l_turn.append(
            "USE " + str(c.instance_id) + " " + str(self.state.l_cards_on_player_board[0].instance_id) + ";")
        self.state.player1.mana -= c.cost
        self.state.l_green_objects_on_player_hand.remove(c)
        self.state.l_cards_on_player_hand.remove(c)


# ------------------------------------------------------------
# Use Red Objects
# ------------------------------------------------------------
class UseRed:
    def __init__(self, state):

        self.state = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        l_cards_can_summon_after = []
        while len(self.state.l_red_objects_on_player_hand) > 0:
            c = self.state.l_red_objects_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_red_objects_on_player_hand.remove(c)
                continue
            if len(self.state.l_cards_on_opponent_board) == 0:
                l_cards_can_summon_after.append(c)
                self.state.l_red_objects_on_player_hand.remove(c)
                continue
            else:
                self.use(c)
        self.state.l_red_objects_on_player_hand = l_cards_can_summon_after

    def use(self, c):
        best_coincidences = 0
        best_coincidence_card = self.state.l_cards_on_opponent_board[0]
        for enemyCard in self.state.l_cards_on_opponent_board:
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
                if best_coincidence_card.lane == self.state.LANE_LEFT:
                    self.state.l_cards_on_left_lane_opponent.remove(best_coincidence_card)
                    if best_coincidence_card in self.state.l_left_opponent_cards_guard:
                        self.state.l_left_opponent_cards_guard.remove(best_coincidence_card)
                else:
                    self.state.l_cards_on_right_lane_opponent.remove(best_coincidence_card)
                    if best_coincidence_card in self.state.l_right_opponent_cards_guard:
                        self.state.l_right_opponent_cards_guard.remove(best_coincidence_card)
                self.state.l_cards_on_opponent_board.remove(best_coincidence_card)

        best_difference = 100
        c_attack = self.state.l_cards_on_opponent_board[0]
        for enemyCard in self.state.l_cards_on_opponent_board:
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
            if c_attack.lane == self.state.LANE_LEFT:
                self.state.l_cards_on_left_lane_opponent.remove(c_attack)
                if c_attack in self.state.l_left_opponent_cards_guard:
                    self.state.l_left_opponent_cards_guard.remove(c_attack)
            else:
                self.state.l_cards_on_right_lane_opponent.remove(c_attack)
                if c_attack in self.state.l_right_opponent_cards_guard:
                    self.state.l_right_opponent_cards_guard.remove(c_attack)
            self.state.l_cards_on_opponent_board.remove(c_attack)
        self.state.l_red_objects_on_player_hand.mana -= c.cost
        self.state.l_cards_on_player_hand.remove(c)


# ------------------------------------------------------------
# Attack strategies class
# ------------------------------------------------------------
# ------------------------------------------------------------
# Destroy all cards before attack head
# ------------------------------------------------------------
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
            self.attack_left_guard(c, 0)
        elif len(self.state.l_cards_on_left_lane_opponent) > 0:
            self.attack_left_cards(c, 0)
        else:
            self.l_turn.append("ATTACK " + str(c.instance_id) + " -1;")
        self.state.l_left_cards_can_attack.remove(c)

    def attack_right(self, n):
        c = self.state.l_right_cards_can_attack[n]
        if len(self.state.l_right_opponent_cards_guard) > 0:
            self.attack_right_guard(c, 0)
        elif len(self.state.l_cards_on_right_lane_opponent) > 0:
            self.attack_right_cards(c, 0)
        else:
            self.l_turn.append("ATTACK " + str(c.instance_id) + " -1;")
        self.state.l_right_cards_can_attack.remove(c)

    def attack_left_guard(self, c, n):
        self.l_turn.append(
            "ATTACK " + str(c.instance_id) + " " + str(self.state.l_left_opponent_cards_guard[n].instance_id) + ";")
        if self.state.l_left_opponent_cards_guard[n].ward:
            self.state.l_left_opponent_cards_guard[n].ward = False
        elif c.lethal:
            self.state.l_left_opponent_cards_guard[n].defense = 0
        else:
            self.state.l_left_opponent_cards_guard[n].defense -= c.attack
        c.defense -= self.state.l_left_opponent_cards_guard[n].attack
        if self.state.l_left_opponent_cards_guard[n].defense <= 0:
            self.state.l_cards_on_left_lane_opponent.remove(self.state.l_left_opponent_cards_guard[n])
            self.state.l_left_opponent_cards_guard.remove(self.state.l_left_opponent_cards_guard[n])
        if c.defense <= 0:
            self.state.l_cards_on_left_lane_player.remove(c)

    def attack_right_guard(self, c, n):
        self.l_turn.append(
            "ATTACK " + str(c.instance_id) + " " + str(self.state.l_right_opponent_cards_guard[n].instance_id) + ";")
        if self.state.l_right_opponent_cards_guard[n].ward:
            self.state.l_right_opponent_cards_guard[n].ward = False
        elif c.lethal:
            self.state.l_right_opponent_cards_guard[n].defense = 0
        else:
            self.state.l_right_opponent_cards_guard[n].defense -= c.attack
        c.defense -= self.state.l_right_opponent_cards_guard[n].attack
        if self.state.l_right_opponent_cards_guard[n].defense <= 0:
            self.state.l_cards_on_right_lane_opponent.remove(self.state.l_right_opponent_cards_guard[n])
            self.state.l_right_opponent_cards_guard.remove(self.state.l_right_opponent_cards_guard[n])
        if c.defense <= 0:
            self.state.l_cards_on_right_lane_player.remove(c)

    def attack_left_cards(self, c, n):
        self.l_turn.append(
            "ATTACK " + str(c.instance_id) + " " + str(self.state.l_cards_on_left_lane_opponent[n].instance_id) + ";")
        if self.state.l_cards_on_left_lane_opponent[n].ward:
            self.state.l_cards_on_left_lane_opponent[n].ward = False
        elif c.lethal:
            self.state.l_cards_on_left_lane_opponent[n].defense = 0
        else:
            self.state.l_cards_on_left_lane_opponent[n].defense -= c.attack
        c.defense -= self.state.l_cards_on_left_lane_opponent[n].attack
        if self.state.l_cards_on_left_lane_opponent[n].defense <= 0:
            self.state.l_cards_on_left_lane_opponent.remove(self.state.l_cards_on_left_lane_opponent[n])
        if c.defense <= 0:
            self.state.l_cards_on_left_lane_player.remove(c)

    def attack_right_cards(self, c, n):
        self.l_turn.append(
            "ATTACK " + str(c.instance_id) + " " + str(self.state.l_cards_on_right_lane_opponent[n].instance_id) + ";")
        if self.state.l_cards_on_right_lane_opponent[n].ward:
            self.state.l_cards_on_right_lane_opponent[n].ward = False
        elif c.lethal:
            self.state.l_cards_on_right_lane_opponent[n].defense = 0
        else:
            self.state.l_cards_on_right_lane_opponent[n].defense -= c.attack
        c.defense -= self.state.l_cards_on_right_lane_opponent[n].attack
        if self.state.l_cards_on_right_lane_opponent[n].defense <= 0:
            self.state.l_cards_on_right_lane_opponent.remove(self.state.l_cards_on_right_lane_opponent[n])
        if c.defense <= 0:
            self.state.l_cards_on_right_lane_player.remove(c)


# ------------------------------------------------------------
# Attack head if you can
# ------------------------------------------------------------
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
            self.l_turn.append(
                "ATTACK " + str(c.instance_id) + " " + str(self.state.l_left_opponent_cards_guard[0].instance_id) + ";")
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
            self.l_turn.append("ATTACK " + str(c.instance_id) + " " + str(
                self.state.l_right_opponent_cards_guard[0].instance_id) + ";")
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

    # ----------------------------------------------
    # Return the string with player data for NN
    # ----------------------------------------------
    def get_str(self):
        s = str(self.hp) + ',' + str(self.mana) + ',' + str(self.cards_remaining) + ',' + str(self.rune) + ',' + str(
            self.draw)
        return s


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
    def get_str(self):
        s = str(self.attack) + ',' + str(self.defense)
        for c in self.abilities:
            s += ','
            if c != '-':
                s += "1"
            else:
                s += "0"
        return s


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
        self.l_guard_creatures_on_player_hand = []  # list of guard creatures on player hand
        self.l_green_objects_on_player_hand = []  # list of green objects on player hand
        self.l_blue_objects_on_player_hand = []  # list of blue objects on player hand
        self.l_red_objects_on_player_hand = []  # list of red objects on player hand
        self.l_cards_on_left_lane_player = []  # list of cards on the left side of the player board
        self.l_cards_on_left_lane_opponent = []  # list of cards on the left side of the opponent board
        self.l_cards_on_right_lane_player = []  # list of cards on the right side of the player board
        self.l_cards_on_right_lane_opponent = []  # list of cards on the right side of the opponent board
        self.l_left_opponent_cards_guard = []  # list of cards on the right side of the opponent board
        self.l_right_opponent_cards_guard = []  # list of cards on the right side of the opponent board
        self.l_left_cards_can_attack = []
        self.l_right_cards_can_attack = []

        self.left_cover = False
        self.right_cover = False

        if not self.is_draft_phase():
            self.classify_cards()

        self.str_info = self.to_str()

    # ---------------------------------------
    # ---------------------------------------
    def get_str(self):
        return self.str_info

    # ---------------------------------------
    # Classify each card in the corresponding list (only if cost <= player mana)
    # Can attack cards on the players lane (already summoned)
    # Can be summoned criatures on the hand
    # Can be used items on the hand
    def classify_cards(self):
        for c in self.l_cards:
            if c.location == self.LOCATION_IN_HAND:
                self.l_cards_on_player_hand.append(c)
                if c.card_type == self.TYPE_CREATURE and c.guard:
                    self.l_guard_creatures_on_player_hand.append(c)
                if c.card_type == self.TYPE_GREEN:
                    self.l_green_objects_on_player_hand.append(c)
                elif c.card_type == self.TYPE_BLUE:
                    self.l_blue_objects_on_player_hand.append(c)
                elif c.card_type == self.TYPE_RED:
                    self.l_red_objects_on_player_hand.append(c)
            elif c.location == self.LOCATION_PLAYER_SIDE and c.lane == self.LANE_LEFT:
                self.l_cards_on_left_lane_player.append(c)
                self.l_left_cards_can_attack.append(c)
                if c.guard:
                    self.left_cover = True
            elif c.location == self.LOCATION_OPPONENT_SIDE and c.lane == self.LANE_LEFT:
                self.l_cards_on_left_lane_opponent.append(c)
                if c.guard:
                    self.l_left_opponent_cards_guard.append(c)
            elif c.location == self.LOCATION_PLAYER_SIDE and c.lane == self.LANE_RIGHT:
                self.l_cards_on_right_lane_player.append(c)
                self.l_right_cards_can_attack.append(c)
                if c.guard:
                    self.right_cover = True
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
    def to_str(self):
        s = self.player1.get_str() + ',' + self.player2.get_str() + ","
        s += self.print_cards_id(self.l_cards_on_player_hand, 8, "0") + ","
        s += self.print_cards_info(self.l_cards_on_left_lane_player, 3, "0,0,0,0,0,0,0,0") + ","
        s += self.print_cards_info(self.l_cards_on_right_lane_player, 3, "0,0,0,0,0,0,0,0") + ","
        s += self.print_cards_info(self.l_cards_on_left_lane_opponent, 3, "0,0,0,0,0,0,0,0") + ","
        s += self.print_cards_info(self.l_cards_on_right_lane_opponent, 3, "0,0,0,0,0,0,0,0")

        return s

    # ----------------------------------------------
    # ----------------------------------------------
    def print_cards_id(self, l_cards, n_cards, no_card):
        s = ""
        i = 0
        for c in l_cards:
            s += str(c.card_id)
            i += 1
            if i < n_cards:
                s += ","

        for j in range(i + 1, n_cards + 1):
            s += no_card
            if j < n_cards:
                s += ","
        return s

    # ----------------------------------------------
    # ----------------------------------------------
    def print_cards_info(self, l_cards, n_cards, no_card):
        s = ""
        i = 0
        for c in l_cards:
            s += c.get_str()
            i += 1
            if i < n_cards:
                s += ","

        for j in range(i + 1, n_cards + 1):
            s += no_card
            if j < n_cards:
                s += ","
        return s


# ------------------------------------------------------------
# Agent
# ------------------------------------------------------------
class Agent:
    def __init__(self):
        self.state = None
        self.last_state = None
        self.draft = Draft()
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
                            int(defense), abilities, (my_health_change), int(opponent_health_change), int(card_draw),
                            int(lane))
            l_cards.append(one_card)

        player1 = Player(player_health1, player_mana1, player_deck1, player_rune1, player_draw1)
        player2 = Player(player_health2, player_mana2, player_deck2, player_rune2, player_draw2)

        self.last_state = copy.copy(self.state)
        self.last_summon_strategy = self.summon_strategy
        self.last_attack_strategy = self.attack_strategy

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
        best_card = self.draft.pick_card(self.state.l_cards)
        print("PICK " + str(best_card))

    # ----------------------------------------------
    # IA for battle
    # ----------------------------------------------
    def ia_battle(self):
        self.summon_strategy = random.randint(1, 33)
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
    def print_NN(self):
        s = self.last_state.get_str() + ','
        s += self.state.get_str() + ','
        s += str(self.last_summon_strategy) + ','
        s += str(self.last_attack_strategy) + ','
        s += str(self.reward())
        return s


if __name__ == '__main__':
    agent = Agent()
    i_turn = 1
    NN = False

    if NN:
        nn_file = open("nn_data.txt", "a")
    while True:
        agent.read_input()
        agent.act()
        if NN and i_turn > 31:
            nn_str = agent.print_NN()
            nn_file.write(nn_str + '\n')
            nn_file.flush()
        i_turn += 1

