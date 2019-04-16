

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
