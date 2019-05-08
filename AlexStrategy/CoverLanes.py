

# ------------------------------------------------------------
# Cover two lanes with guard
# ------------------------------------------------------------
class CoverLanes:
    def __init__(self, state):

        self.state = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        if self.state.left_cover is not True and len(self.state.l_cards_on_left_lane_player) < 3:
            self.cover_left()
        if self.state.right_cover is not True and len(self.state.l_cards_on_right_lane_player) < 3:
            self.cover_right()
        return self.l_turn

    def cover_left(self):
        while len(self.state.l_guard_creatures_on_player_hand) > 0:
            c = self.state.l_guard_creatures_on_player_hand[0]
            if c.cost > self.state.player1.mana or c not in self.state.l_cards_on_player_hand:
                self.state.l_guard_creatures_on_player_hand.remove(c)
                continue
            else:
                self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_LEFT) + ";")
                if c.charge:
                    self.state.l_left_cards_can_attack.append(c)
            self.state.l_cards_on_left_lane_player.append(c)
            self.state.player2.hp += c.opponent_health_change
            self.state.player1.hp += c.my_health_change
            self.state.player1.draw += c.card_draw
            self.state.player1.mana -= c.cost
            self.state.l_guard_creatures_on_player_hand.remove(c)
            self.state.l_cards_on_player_hand.remove(c)
            self.state.left_cover = True
            return

    def cover_right(self):
        while len(self.state.l_guard_creatures_on_player_hand) > 0:
            c = self.state.l_guard_creatures_on_player_hand[0]
            if c.cost > self.state.player1.mana or c not in self.state.l_cards_on_player_hand:
                self.state.l_guard_creatures_on_player_hand.remove(c)
                continue
            else:
                self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_RIGHT) + ";")
                if c.charge:
                    self.state.l_right_cards_can_attack.append(c)
            self.state.l_cards_on_right_lane_player.append(c)
            self.state.player2.hp += c.opponent_health_change
            self.state.player1.hp += c.my_health_change
            self.state.player1.draw += c.card_draw
            self.state.player1.mana -= c.cost
            self.state.l_guard_creatures_on_player_hand.remove(c)
            self.state.l_cards_on_player_hand.remove(c)
            self.state.right_cover = True
            return
