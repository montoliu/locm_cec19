

# ------------------------------------------------------------
# Use blue objects
# ------------------------------------------------------------
class UseBlue:
    def __init__(self, state):

        self.state = state
        self.l_turn = []
        self.l_cards_on_opponent_board = []
        self.get_turn()

    def get_turn(self):
        if len(self.state.l_cards_on_left_lane_opponent) > 0:
            self.l_cards_on_opponent_board += self.state.l_cards_on_left_lane_opponent
        if len(self.state.l_cards_on_right_lane_opponent) > 0:
            self.l_cards_on_opponent_board += self.state.l_cards_on_right_lane_opponent
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
        if c.defense < 0 and len(self.l_cards_on_opponent_board) > 0:
            best_difference = 30
            c_attack = self.l_cards_on_opponent_board[0]
            for enemyCard in self.l_cards_on_opponent_board:
                diference = abs(enemyCard.defense + c.defense)
                if diference == 0:
                    c_attack = enemyCard
                    break
                elif diference < best_difference:
                    best_difference = diference
                    c_attack = enemyCard
            self.l_turn.append("USE " + str(c.instance_id) + " " + str(c_attack.instance_id) + ";")
            c_attack.defense += c.defense
            c_attack.attack += c.attack
            self.state.player2.hp += c.opponent_health_change
            self.state.player1.hp += c.my_health_change
            self.state.player1.draw += c.card_draw
            if c_attack.defense <= 0:
                if c_attack.lane == self.state.LANE_LEFT:
                    self.state.l_cards_on_left_lane_opponent.remove(c_attack)
                    if c_attack in self.state.l_left_opponent_cards_guard:
                        self.state.l_left_opponent_cards_guard.remove(c_attack)
                    if c_attack in self.state.l_left_opponent_cards_drain:
                        self.state.l_left_opponent_cards_drain.remove(c_attack)
                    if c_attack in self.state.l_left_opponent_cards_lethal:
                        self.state.l_left_opponent_cards_lethal.remove(c_attack)
                else:
                    self.state.l_cards_on_right_lane_opponent.remove(c_attack)
                    if c_attack in self.state.l_right_opponent_cards_guard:
                        self.state.l_right_opponent_cards_guard.remove(c_attack)
                    if c_attack in self.state.l_right_opponent_cards_drain:
                        self.state.l_right_opponent_cards_drain.remove(c_attack)
                    if c_attack in self.state.l_right_opponent_cards_lethal:
                        self.state.l_right_opponent_cards_lethal.remove(c_attack)
                self.l_cards_on_opponent_board.remove(c_attack)
        else:
            self.l_turn.append("USE " + str(c.instance_id) + " -1;")
            self.state.player2.hp += c.defense
            self.state.player2.hp += c.opponent_health_change
            self.state.player1.hp += c.my_health_change
            self.state.player1.draw += c.card_draw
        self.state.player1.mana -= c.cost
        self.state.l_blue_objects_on_player_hand.remove(c)
