

# ------------------------------------------------------------
# Use green objects
# ------------------------------------------------------------
class UseGreen:
    def __init__(self, state):

        self.state = state
        self.l_turn = []
        self.l_cards_on_player_board = []
        self.get_turn()

    def get_turn(self):
        l_cards_can_summon_after = []
        if len(self.state.l_cards_on_left_lane_player) > 0:
            self.l_cards_on_player_board += self.state.l_cards_on_left_lane_player
        if len(self.state.l_cards_on_right_lane_player) > 0:
            self.l_cards_on_player_board += self.state.l_cards_on_right_lane_player
        while len(self.state.l_green_objects_on_player_hand) > 0:
            c = self.state.l_green_objects_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_green_objects_on_player_hand.remove(c)
                continue
            if len(self.l_cards_on_player_board) == 0:
                l_cards_can_summon_after.append(c)
                self.state.l_green_objects_on_player_hand.remove(c)
                continue
            else:
                self.use(c)
        self.state.l_green_objects_on_player_hand = l_cards_can_summon_after

    def use(self, c):
        self.l_cards_on_player_board.sort(key=lambda x: x.cost, reverse=True)
        self.l_turn.append("USE " + str(c.instance_id) + " " + str(self.l_cards_on_player_board[0].instance_id) + ";")
        self.l_cards_on_player_board[0].defense += c.defense
        self.l_cards_on_player_board[0].attack += c.attack
        if c.breakthrough:
            self.l_cards_on_player_board[0].breakthrough = True
        if c.charge:
            self.l_cards_on_player_board[0].charge = True
            if self.l_cards_on_player_board[0].lane == self.state.LANE_LEFT and self.l_cards_on_player_board[
                0] not in self.state.l_left_cards_can_attack:
                self.state.l_left_cards_can_attack.append(self.l_cards_on_player_board[0])
            elif self.l_cards_on_player_board[0].lane == self.state.LANE_RIGHT and self.l_cards_on_player_board[
                0] not in self.state.l_right_cards_can_attack:
                self.state.l_right_cards_can_attack.append(self.l_cards_on_player_board[0])
        if c.drain:
            self.l_cards_on_player_board[0].drain = True
        if c.guard:
            self.l_cards_on_player_board[0].guard = True
        if c.lethal:
            self.l_cards_on_player_board[0].lethal = True
        if c.ward:
            self.l_cards_on_player_board[0].ward = True
        self.state.player2.hp += c.opponent_health_change
        self.state.player1.hp += c.my_health_change
        self.state.player1.draw += c.card_draw
        self.state.player1.mana -= c.cost
        self.state.l_green_objects_on_player_hand.remove(c)
