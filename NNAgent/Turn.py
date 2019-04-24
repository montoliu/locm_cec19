import AttackHead as ah
import AttackCards as ac
import SummonLeft as sl
import SummonRight as sr
import SummonBalanced as sb
import CoverLanes as cl
import UseGreen as ug
import UseRed as ur
import UseBlue as ub
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
        self.use_mana(self.summon_strategy)
        self.attack()
        if len(self.turn_state.l_cards_on_player_hand) + len(self.turn_state.l_green_objects_on_player_hand) + len(self.turn_state.l_blue_objects_on_player_hand) +len(self.turn_state.l_red_objects_on_player_hand)> 0:
            self.use_mana(self.summon_strategy)
            self.attack()

    def use_mana(self, strategy):
        if strategy == 1:
            # Summon two lanes balanced
            summon_turn = sb.SummonBalanced(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif strategy == 2:
            # Summon only left
            summon_turn = sl.SummonLeft(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif strategy == 3:
            # Summon only right
            summon_turn = sr.SummonRight(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif strategy == 4:
            # Summon trying cover two lanes with guard and after summon two lanes balanced
            # summon_turn = scb.SummonCoverOrBalanced(self.turn_state)
            summon_turn = cl.CoverLanes(self.turn_state)
            self.l_turn += summon_turn.l_turn
            self.use_mana(1)
        elif strategy == 5:
            # Summon trying cover two lanes with guard and after summon only left
            # summon_turn = scl.SummonCoverOrLeft(self.turn_state)
            summon_turn = cl.CoverLanes(self.turn_state)
            self.l_turn += summon_turn.l_turn
            self.use_mana(2)
        elif strategy == 6:
            # Summon trying cover two lanes with guard and after summon only right
            # summon_turn = scr.SummonCoverOrRight(self.turn_state)
            summon_turn = cl.CoverLanes(self.turn_state)
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
            summon_turn = ug.UseGreen(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif strategy == 20:
            # Only use red objects
            summon_turn = ur.UseRed(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif strategy == 21:
            # Only use blue objects
            summon_turn = ub.UseBlue(self.turn_state)
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
            #use abjects G-R-B and cover/balanced cost <
            self.use_mana(28)
            self.use_mana(7)
    ##Aqui añadire combinaciones

    def attack(self):
        if self.attack_strategy == 1:
            attack_turn = ah.AttackHead(self.turn_state)
            self.l_turn += attack_turn.l_turn
        elif self.attack_strategy == 2:
            attack_turn = ac.AttackCards(self.turn_state)
            self.l_turn += attack_turn.l_turn
