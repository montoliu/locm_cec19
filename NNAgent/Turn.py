import AttackHead as ah
import AttackCards as ac
import SummonLeft as sl
import SummonRight as sr
import SummonBalanced as sb
import SummonCoverOrBalanced as scb
import SummonCoverOrLeft as scl
import SummonCoverOrRight as scr

import copy


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
            summon_turn = sb.SummonBalanced(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif self.summon_strategy == 2:
            summon_turn = sl.SummonLeft(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif self.summon_strategy == 3:
            summon_turn = sr.SummonRight(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif self.summon_strategy == 4:
            summon_turn = scb.SummonCoverOrBalanced(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif self.summon_strategy == 5:
            summon_turn = scl.SummonCoverOrLeft(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif self.summon_strategy == 6:
            summon_turn = scr.SummonCoverOrRight(self.turn_state)
            self.l_turn += summon_turn.l_turn

    def attack(self):
        if self.attack_strategy == 1:
            attack_turn = ah.AttackHead(self.turn_state)
            self.l_turn += attack_turn.l_turn
        elif self.attack_strategy == 2:
            attack_turn = ac.AttackCards(self.turn_state)
            self.l_turn += attack_turn.l_turn
