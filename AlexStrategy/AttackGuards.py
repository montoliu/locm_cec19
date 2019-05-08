

# ------------------------------------------------------------
# Attack only guard cards
# ------------------------------------------------------------
class AttackGuards:
    def __init__(self, state):

        self.state = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        while len(self.state.l_left_cards_can_attack) > 0 and len(self.state.l_left_opponent_cards_guard) > 0:
            self.attack_left(0)
        while len(self.state.l_right_cards_can_attack) > 0 and len(self.state.l_right_opponent_cards_guard) > 0:
            self.attack_right(0)

    def attack_left(self, n):
        c = self.state.l_left_cards_can_attack[n]
        self.attack_left_guard(c, 0)
        self.state.l_left_cards_can_attack.remove(c)

    def attack_right(self, n):
        c = self.state.l_right_cards_can_attack[n]
        self.attack_right_guard(c, 0)
        self.state.l_right_cards_can_attack.remove(c)

    def attack_left_guard(self, c, n):
        self.l_turn.append(
            "ATTACK " + str(c.instance_id) + " " + str(self.state.l_left_opponent_cards_guard[n].instance_id) + ";")
        if self.state.l_left_opponent_cards_guard[n].ward:
            self.state.l_left_opponent_cards_guard[n].ward = False
        elif c.lethal:
            self.state.l_left_opponent_cards_guard[n].defense = 0
            if c.drain:
                self.state.player1.hp += c.attack
        else:
            self.state.l_left_opponent_cards_guard[n].defense -= c.attack
            if c.drain:
                self.state.player1.hp += c.attack
        c.defense -= self.state.l_left_opponent_cards_guard[n].attack
        if self.state.l_left_opponent_cards_guard[n].defense <= 0:
            if c.breakthrough:
                self.state.player2.hp += self.state.l_left_opponent_cards_guard[n].defense
            self.state.l_cards_on_left_lane_opponent.remove(self.state.l_left_opponent_cards_guard[n])
            if self.state.l_left_opponent_cards_guard[n] in self.state.l_left_opponent_cards_drain:
                self.state.l_left_opponent_cards_drain.remove(self.state.l_left_opponent_cards_guard[n])
            if self.state.l_left_opponent_cards_guard[n] in self.state.l_left_opponent_cards_lethal:
                self.state.l_left_opponent_cards_lethal.remove(self.state.l_left_opponent_cards_guard[n])
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
            if c.drain:
                self.state.player1.hp += c.attack
        else:
            self.state.l_right_opponent_cards_guard[n].defense -= c.attack
            if c.drain:
                self.state.player1.hp += c.attack
        c.defense -= self.state.l_right_opponent_cards_guard[n].attack
        if self.state.l_right_opponent_cards_guard[n].defense <= 0:
            if c.breakthrough:
                self.state.player2.hp += self.state.l_right_opponent_cards_guard[n].defense
            self.state.l_cards_on_right_lane_opponent.remove(self.state.l_right_opponent_cards_guard[n])
            if self.state.l_right_opponent_cards_guard[n] in self.state.l_right_opponent_cards_drain:
                self.state.l_right_opponent_cards_drain.remove(self.state.l_right_opponent_cards_guard[n])
            if self.state.l_right_opponent_cards_guard[n] in self.state.l_right_opponent_cards_lethal:
                self.state.l_right_opponent_cards_lethal.remove(self.state.l_right_opponent_cards_guard[n])
            self.state.l_right_opponent_cards_guard.remove(self.state.l_right_opponent_cards_guard[n])
        if c.defense <= 0:
            self.state.l_cards_on_right_lane_player.remove(c)
