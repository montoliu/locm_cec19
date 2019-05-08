

# ------------------------------------------------------------
# Attack only drain cards
# ------------------------------------------------------------
class AttackDrains:
    def __init__(self, state):

        self.state = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        while len(self.state.l_left_cards_can_attack) > 0 and len(self.state.l_left_opponent_cards_drain) > 0:
            self.attack_left(0)
        while len(self.state.l_right_cards_can_attack) > 0 and len(self.state.l_right_opponent_cards_drain) > 0:
            self.attack_right(0)

    def attack_left(self, n):
        c = self.state.l_left_cards_can_attack[n]
        self.attack_left_drain(c, 0)
        self.state.l_left_cards_can_attack.remove(c)

    def attack_right(self, n):
        c = self.state.l_right_cards_can_attack[n]
        self.attack_right_drain(c, 0)
        self.state.l_right_cards_can_attack.remove(c)

    def attack_left_drain(self, c, n):
        self.l_turn.append(
            "ATTACK " + str(c.instance_id) + " " + str(self.state.l_left_opponent_cards_drain[n].instance_id) + ";")
        if self.state.l_left_opponent_cards_drain[n].ward:
            self.state.l_left_opponent_cards_drain[n].ward = False
        elif c.lethal:
            self.state.l_left_opponent_cards_drain[n].defense = 0
            if c.drain:
                self.state.player1.hp += c.attack
        else:
            self.state.l_left_opponent_cards_drain[n].defense -= c.attack
            if c.drain:
                self.state.player1.hp += c.attack
        c.defense -= self.state.l_left_opponent_cards_drain[n].attack
        if self.state.l_left_opponent_cards_drain[n].defense <= 0:
            if c.breakthrough:
                self.state.player2.hp += self.state.l_left_opponent_cards_drain[n].defense
            self.state.l_cards_on_left_lane_opponent.remove(self.state.l_left_opponent_cards_drain[n])
            if self.state.l_left_opponent_cards_drain[n] in self.state.l_left_opponent_cards_guard:
                self.state.l_left_opponent_cards_guard.remove(self.state.l_left_opponent_cards_drain[n])
            if self.state.l_left_opponent_cards_drain[n] in self.state.l_left_opponent_cards_lethal:
                self.state.l_left_opponent_cards_lethal.remove(self.state.l_left_opponent_cards_drain[n])
            self.state.l_left_opponent_cards_drain.remove(self.state.l_left_opponent_cards_drain[n])
        if c.defense <= 0:
            self.state.l_cards_on_left_lane_player.remove(c)

    def attack_right_drain(self, c, n):
        self.l_turn.append(
            "ATTACK " + str(c.instance_id) + " " + str(self.state.l_right_opponent_cards_drain[n].instance_id) + ";")
        if self.state.l_right_opponent_cards_drain[n].ward:
            self.state.l_right_opponent_cards_drain[n].ward = False
        elif c.lethal:
            self.state.l_right_opponent_cards_drain[n].defense = 0
            if c.drain:
                self.state.player1.hp += c.attack
        else:
            self.state.l_right_opponent_cards_drain[n].defense -= c.attack
            if c.drain:
                self.state.player1.hp += c.attack
        c.defense -= self.state.l_right_opponent_cards_drain[n].attack
        if self.state.l_right_opponent_cards_drain[n].defense <= 0:
            if c.breakthrough:
                self.state.player2.hp += self.state.l_right_opponent_cards_drain[n].defense
            self.state.l_cards_on_right_lane_opponent.remove(self.state.l_right_opponent_cards_drain[n])
            if self.state.l_right_opponent_cards_drain[n] in self.state.l_right_opponent_cards_guard:
                self.state.l_right_opponent_cards_guard.remove(self.state.l_right_opponent_cards_drain[n])
            if self.state.l_right_opponent_cards_drain[n] in self.state.l_right_opponent_cards_lethal:
                self.state.l_right_opponent_cards_lethal.remove(self.state.l_right_opponent_cards_drain[n])
            self.state.l_right_opponent_cards_drain.remove(self.state.l_right_opponent_cards_drain[n])
        if c.defense <= 0:
            self.state.l_cards_on_right_lane_player.remove(c)
