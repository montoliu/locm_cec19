import random


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
                self.state.l_cards_on_player_hand.remove(c)
                continue
            elif c.card_type == self.state.TYPE_CREATURE:
                self.summon(c)
            else:
                self.state.l_cards_on_player_hand.remove(c)
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
