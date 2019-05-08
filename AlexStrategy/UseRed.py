

# ------------------------------------------------------------
# Use Red Objects
# ------------------------------------------------------------
class UseRed:
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
        while len(self.state.l_red_objects_on_player_hand) > 0:
            c = self.state.l_red_objects_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_red_objects_on_player_hand.remove(c)
                continue
            if len(self.l_cards_on_opponent_board) == 0:
                l_cards_can_summon_after.append(c)
                self.state.l_red_objects_on_player_hand.remove(c)
                continue
            else:
                self.use(c)
        self.state.l_red_objects_on_player_hand = l_cards_can_summon_after

    def use(self, c):
        best_coincidences = 0
        best_coincidence_card = self.l_cards_on_opponent_board[0]
        for enemyCard in self.l_cards_on_opponent_board:
            coincidences = 0
            if enemyCard.breakthrough and c.breakthrough:
                coincidences += 1
            if enemyCard.charge and c.charge:
                coincidences += 1
            if enemyCard.drain and c.drain:
                coincidences += 1
            if enemyCard.guard and c.guard:
                coincidences += 1
            if enemyCard.lethal and c.lethal:
                coincidences += 1
            if enemyCard.ward and c.ward:
                coincidences += 1
            if coincidences > best_coincidences:
                best_coincidences = coincidences
                best_coincidence_card = enemyCard

        if best_coincidences > 0:
            self.l_turn.append("USE " + str(c.instance_id) + " " + str(best_coincidence_card.instance_id) + ";")
            best_coincidence_card.defense += c.defense
            best_coincidence_card.attack += c.attack
            if best_coincidence_card.breakthrough and c.breakthrough:
                best_coincidence_card.breakthrough = False
            if best_coincidence_card.charge and c.charge:
                best_coincidence_card.charge = False
            if best_coincidence_card.drain and c.drain:
                best_coincidence_card.drain = False
            if best_coincidence_card.guard and c.guard:
                best_coincidence_card.guard = False
            if best_coincidence_card.lethal and c.lethal:
                best_coincidence_card.lethal = False
            if best_coincidence_card.ward and c.ward:
                best_coincidence_card.ward = False
            self.state.player2.hp += c.opponent_health_change
            self.state.player1.hp += c.my_health_change
            self.state.player1.draw += c.card_draw
            if best_coincidence_card.defense <= 0:
                if best_coincidence_card.lane == self.state.LANE_LEFT:
                    self.state.l_cards_on_left_lane_opponent.remove(best_coincidence_card)
                    if best_coincidence_card in self.state.l_left_opponent_cards_guard:
                        self.state.l_left_opponent_cards_guard.remove(best_coincidence_card)
                    if best_coincidence_card in self.state.l_left_opponent_cards_drain:
                        self.state.l_left_opponent_cards_drain.remove(best_coincidence_card)
                    if best_coincidence_card in self.state.l_left_opponent_cards_lethal:
                        self.state.l_left_opponent_cards_lethal.remove(best_coincidence_card)
                else:
                    self.state.l_cards_on_right_lane_opponent.remove(best_coincidence_card)
                    if best_coincidence_card in self.state.l_right_opponent_cards_guard:
                        self.state.l_right_opponent_cards_guard.remove(best_coincidence_card)
                    if best_coincidence_card in self.state.l_right_opponent_cards_drain:
                        self.state.l_right_opponent_cards_drain.remove(best_coincidence_card)
                    if best_coincidence_card in self.state.l_right_opponent_cards_lethal:
                        self.state.l_right_opponent_cards_lethal.remove(best_coincidence_card)
                self.l_cards_on_opponent_board.remove(best_coincidence_card)
        else:
            best_difference = 100
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
                    if best_coincidence_card in self.state.l_left_opponent_cards_drain:
                        self.state.l_left_opponent_cards_drain.remove(best_coincidence_card)
                    if best_coincidence_card in self.state.l_left_opponent_cards_lethal:
                        self.state.l_left_opponent_cards_lethal.remove(best_coincidence_card)
                else:
                    self.state.l_cards_on_right_lane_opponent.remove(c_attack)
                    if c_attack in self.state.l_right_opponent_cards_guard:
                        self.state.l_right_opponent_cards_guard.remove(c_attack)
                    if best_coincidence_card in self.state.l_right_opponent_cards_drain:
                        self.state.l_right_opponent_cards_drain.remove(best_coincidence_card)
                    if best_coincidence_card in self.state.l_right_opponent_cards_lethal:
                        self.state.l_right_opponent_cards_lethal.remove(best_coincidence_card)
                self.l_cards_on_opponent_board.remove(c_attack)
        self.state.player1.mana -= c.cost
        self.state.l_red_objects_on_player_hand.remove(c)
