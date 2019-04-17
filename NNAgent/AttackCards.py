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
