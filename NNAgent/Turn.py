import Strategies.AttackHead as ah
import Strategies.AttackCards as ac
import Strategies.SummonLeft as sl
import Strategies.SummonRight as sr
import Strategies.SummonBalanced as sb
import copy
# ------------------------------------------------------------
# Turn information
# ------------------------------------------------------------
class Turn:
    def __init__(self, state, summon_strategy, attack_strategy):

        self.state = copy.copy(state)
        self.summon_strategy = summon_strategy
        self.attack_strategy = attack_strategy
        self.l_turn = []
        self.create_turn()

    def create_turn(self):
        self.use_mana()
        self.attack()
        if len(self.state.l_cards_on_player_hand) > 0:
            self.use_mana()
            self.attack()

    def use_mana(self):
        if self.summon_strategy == 0:
            summon_turn = sb.SummonBalanced(self.state)
            self.l_turn.append(summon_turn.l_turn)
        elif self.summon_strategy == 1:
            summon_turn = sl.SummonLeft(self.state)
            self.l_turn.append(summon_turn.l_turn)
        elif self.summon_strategy == 2:
            summon_turn = sr.SummonRight(self.state)
            self.l_turn.append(summon_turn.l_turn)

    def attack(self):
        if self.attack_strategy == 0:
            attack_turn = ah.AttackHead(self.state)
            self.l_turn.append(attack_turn.l_turn)
        elif self.attack_strategy == 1:
            attack_turn = ac.AttackCards(self.state)
            self.l_turn.append(attack_turn.l_turn)












  #       self.turn = None
  # def ia_battle(self):
  #       self.turn = tr.Turn(self.state, self.summon_strategy, self.attack_strategy)
  #       if len(self.turn.l_turn) == 0:
  #           print ("PASS")
  #       else:
  #           turn_string = ""
  #           for action in self.state.l_turn:
  #               turn_string += action
  #           print(turn_string)
