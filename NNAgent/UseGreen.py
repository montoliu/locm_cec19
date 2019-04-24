

# ------------------------------------------------------------
# Use green objects
# ------------------------------------------------------------
class UseGreen:
    def __init__(self, state):

        self.state = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        l_cards_can_summon_after = []
        while len(self.state.l_green_objects_on_player_hand) > 0:
            c = self.state.l_green_objects_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_cards_on_player_hand.remove(c)
                continue
            if len(self.state.l_cards_on_player_board) == 0:
                l_cards_can_summon_after.append(c)
                self.state.l_green_objects_on_player_hand.remove(c)
                continue
            else:
                self.use(c)
        self.state.l_green_objects_on_player_hand = l_cards_can_summon_after

    def use(self, c):
        self.state.l_cards_on_player_board.sort(key=lambda x: x.cost, reverse=True)
        self.l_turn.append("USE " + str(c.instance_id) + " " + str(self.state.l_cards_on_player_board[0].instance_id) + ";")
        self.state.player1.mana -= c.cost
        self.state.l_green_objects_on_player_hand.remove(c)
        self.state.l_cards_on_player_hand.remove(c)
