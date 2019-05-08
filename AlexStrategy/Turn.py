import AttackHead as ah
import AttackDrains as ad
import AttackLethals as al
import AttackGuards as ag
import AttackCards as ac

import SummonLeft as sl
import SummonRight as sr
import SummonBalanced as sb
import CoverLanes as cl
import UseGreen as ug
import UseRed as ur
import UseBlue as ub
import SummonUse as su

import copy


# ------------------------------------------------------------
# Turn information
# ------------------------------------------------------------
class Turn:
    def __init__(self, state, summon_strategy, attack_strategy):
        self.state = state
        self.turn_state = copy.deepcopy(state)
        self.summon_strategy = summon_strategy
        self.attack_strategy = attack_strategy
        self.l_turn = []
        self.create_turn()
        self.reward = self.evaluate_turn()

    def create_turn(self):
        self.use_mana(self.summon_strategy)
        self.attack(self.attack_strategy)
        if len(self.turn_state.l_cards_on_player_hand) + len(self.turn_state.l_green_objects_on_player_hand) + len(self.turn_state.l_blue_objects_on_player_hand) +len(self.turn_state.l_red_objects_on_player_hand)> 0:
            self.use_mana(self.summon_strategy)
            self.attack(self.attack_strategy)

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
            # Summon left and after summon right and use objects G-R-B
            self.use_mana(2)
            self.use_mana(3)
            self.use_mana(30)
        elif strategy == 20:
            # Summon right and after summon left and use objects G-R-B
            self.use_mana(3)
            self.use_mana(2)
            self.use_mana(30)
        elif strategy == 21:
            # Cover/balanced cost < and use objects G-R-B
            self.use_mana(13)
            self.use_mana(30)
        elif strategy == 22:
            # Cover/balanced cost < and use objects B-R-G
            self.use_mana(13)
            self.use_mana(27)
        elif strategy == 23:
            # Use objects G-R-B and cover/balanced cost <
            self.use_mana(30)
            self.use_mana(13)
        elif strategy == 24:
            # use abjects G-R-B and cover/balanced cost <
            self.use_mana(30)
            self.use_mana(13)
        elif strategy == 25:
            # use objects B-R-G and balanced cost <
            self.use_mana(35)
            self.use_mana(7)
        elif strategy == 26:
            # balanced cost > and use objects G-R-B
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
            self.turn_state.l_guard_creatures_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
            self.use_mana(1)
            self.use_mana(30)
        elif strategy == 27:
            # Summon/Use like alexAgent
            summon_turn = su.SummonUse(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif strategy == 28:
            # Only use green objects
            summon_turn = ug.UseGreen(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif strategy == 29:
            # Only use red objects
            summon_turn = ur.UseRed(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif strategy == 36:
            # Only use blue objects
            summon_turn = ub.UseBlue(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif strategy == 30:
            # Only use green, red and blue objects
            self.use_mana(28)
            self.use_mana(29)
            self.use_mana(36)
        elif strategy == 31:
            # Only use green, blue and red objects
            self.use_mana(28)
            self.use_mana(36)
            self.use_mana(29)
        elif strategy == 32:
            # Only use red, green and blue objects
            self.use_mana(29)
            self.use_mana(28)
            self.use_mana(36)
        elif strategy == 33:
            # Only use red, blue and green objects
            self.use_mana(29)
            self.use_mana(35)
            self.use_mana(28)
        elif strategy == 34:
            # Only use blue, green and red objects
            self.use_mana(36)
            self.use_mana(28)
            self.use_mana(29)
        elif strategy == 35:
            # Only use blue, red and green objects
            self.use_mana(36)
            self.use_mana(29)
            self.use_mana(28)

    def attack(self, strategy):
        if strategy == 1:
            # Attack the head if I can
            attack_turn = ah.AttackHead(self.turn_state)
            self.l_turn += attack_turn.l_turn
        elif strategy == 2:
            # Attack the enemy cards before attack head
            attack_turn = ac.AttackCards(self.turn_state)
            self.l_turn += attack_turn.l_turn
        elif strategy == 3:
            # Attack the enemy cards before attack head our cards sort by attack >
            self.turn_state.l_left_cards_can_attack.sort(key=lambda x: x.attack, reverse=True)
            self.turn_state.l_right_cards_can_attack.sort(key=lambda x: x.attack, reverse=True)
            self.attack(2)
        elif strategy == 4:
            # Attack the enemy cards before attack head his cards sort by defense <
            self.turn_state.l_cards_on_right_lane_opponent.sort(key=lambda x: x.defense, reverse=False)
            self.turn_state.l_cards_on_left_lane_opponent.sort(key=lambda x: x.attack, reverse=False)
            self.turn_state.l_left_opponent_cards_guard.sort(key=lambda x: x.defense, reverse=False)
            self.turn_state.l_right_opponent_cards_guard.sort(key=lambda x: x.defense, reverse=False)
            self.attack(2)
        elif strategy == 5:
            # Attack the enemy cards before attack head our cards sort by attack > and  his cards sort by defense <
            self.turn_state.l_left_cards_can_attack.sort(key=lambda x: x.attack, reverse=True)
            self.turn_state.l_right_cards_can_attack.sort(key=lambda x: x.attack, reverse=True)
            self.turn_state.l_cards_on_right_lane_opponent.sort(key=lambda x: x.defense, reverse=False)
            self.turn_state.l_cards_on_left_lane_opponent.sort(key=lambda x: x.attack, reverse=False)
            self.turn_state.l_left_opponent_cards_guard.sort(key=lambda x: x.defense, reverse=False)
            self.turn_state.l_right_opponent_cards_guard.sort(key=lambda x: x.defense, reverse=False)
            self.attack(2)
        elif strategy == 6:
            # Attack the drain cards after guards and head
            attack_turn = ag.AttackGuards(self.turn_state)
            self.l_turn += attack_turn.l_turn
            attack_turn = ad.AttackDrains(self.turn_state)
            self.l_turn += attack_turn.l_turn
            self.attack(1)
        elif strategy == 7:
            # Attack the lethal cards after guards and head
            attack_turn = ag.AttackGuards(self.turn_state)
            self.l_turn += attack_turn.l_turn
            attack_turn = al.AttackLethals(self.turn_state)
            self.l_turn += attack_turn.l_turn
            self.attack(1)
        elif strategy == 8:
            # Attack the guards, drain, lethal and head
            attack_turn = ag.AttackGuards(self.turn_state)
            self.l_turn += attack_turn.l_turn
            attack_turn = ad.AttackDrains(self.turn_state)
            self.l_turn += attack_turn.l_turn
            attack_turn = al.AttackLethals(self.turn_state)
            self.l_turn += attack_turn.l_turn
            self.attack(1)
        elif strategy == 9:
            # Attack the guards, drain, lethal and head sort our cards by attack > and  his cards sort by defense <
            self.turn_state.l_left_cards_can_attack.sort(key=lambda x: x.attack, reverse=True)
            self.turn_state.l_right_cards_can_attack.sort(key=lambda x: x.attack, reverse=True)
            self.turn_state.l_cards_on_right_lane_opponent.sort(key=lambda x: x.defense, reverse=False)
            self.turn_state.l_cards_on_left_lane_opponent.sort(key=lambda x: x.defense, reverse=False)
            self.turn_state.l_left_opponent_cards_guard.sort(key=lambda x: x.defense, reverse=False)
            self.turn_state.l_right_opponent_cards_guard.sort(key=lambda x: x.defense, reverse=False)
            self.attack(8)

    # ------------------------------------------------------------
    # Calculate the reward of the turn
    # ------------------------------------------------------------
    def evaluate_turn(self):
        reward = 0
        if self.turn_state.player2.hp <= 0:
            return 1000
        reward += self.turn_state.player1.hp - self.state.player1.hp
        reward += self.turn_state.player1.draw - self.state.player1.draw
        reward += self.state.player2.hp - self.turn_state.player2.hp
        reward += self.turn_state.player_cardvalue() - self.state.player_cardvalue()
        reward += self.state.opponent_cardvalue() - self.turn_state.opponent_cardvalue()
        return reward
