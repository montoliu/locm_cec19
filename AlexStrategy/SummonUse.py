import random


# ------------------------------------------------------------
# Summon/Use like AlexAgent
# ------------------------------------------------------------
class SummonUse:
    def __init__(self, state):

        self.state = state
        self.l_turn = []
        self.l_cards_on_player_board = []
        self.l_cards_on_opponent_board = []
        self.get_turn()

    def get_turn(self):
        self.l_cards_on_player_board = self.state.l_cards_on_left_lane_player + self.state.l_cards_on_right_lane_player
        self.l_cards_on_opponent_board = self.state.l_cards_on_right_lane_opponent + self.state.l_cards_on_right_lane_opponent
        if len(self.l_cards_on_player_board) < 3:
            self.state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=False)
        else:
            self.state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
        l_cards_can_summon_after = []
        if self.state.left_cover is not True and len(self.state.l_cards_on_left_lane_player) < 3:
            self.cover_left()
        if self.state.right_cover is not True and len(self.state.l_cards_on_right_lane_player) < 3:
            self.cover_right()
        while len(self.state.l_cards_on_player_hand) > 0:
            c = self.state.l_cards_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_cards_on_player_hand.remove(c)
                continue
            if c.card_type == self.state.TYPE_CREATURE and len(self.l_cards_on_player_board) >= 6:
                self.state.l_cards_on_player_hand.remove(c)
                l_cards_can_summon_after.append(c)
                continue
            if c.card_type == self.state.TYPE_GREEN and len(self.l_cards_on_player_board) == 0:
                self.state.l_cards_on_player_hand.remove(c)
                continue
            if c.card_type == self.state.TYPE_RED and len(self.l_cards_on_opponent_board) == 0:
                self.state.l_cards_on_player_hand.remove(c)
                continue
            if c.card_type == self.state.TYPE_CREATURE:
                self.summon(c)
            elif c.card_type == self.state.TYPE_GREEN:
                self.use_green(c)
            elif c.card_type == self.state.TYPE_RED:
                self.use_red(c)
            elif c.card_type == self.state.TYPE_BLUE:
                self.use_blue(c)
        self.state.l_cards_on_player_hand = l_cards_can_summon_after

    def summon(self, c):
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
        self.l_cards_on_player_board.append(c)
        self.state.player2.hp += c.opponent_health_change
        self.state.player1.hp += c.my_health_change
        self.state.player1.draw += c.card_draw
        self.state.player1.mana -= c.cost
        self.state.l_cards_on_player_hand.remove(c)

    def summon_right(self, c):
        self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_RIGHT) + ";")
        if c.charge:
            self.state.l_right_cards_can_attack.append(c)
        # if c.guard:
        #    self.left_cover = True
        self.state.l_cards_on_right_lane_player.append(c)

    def summon_left(self, c):
        self.l_turn.append("SUMMON " + str(c.instance_id) + " " + str(self.state.LANE_LEFT) + ";")
        if c.charge:
            self.state.l_left_cards_can_attack.append(c)
        # if c.guard:
        #    self.left_cover = True
        self.state.l_cards_on_left_lane_player.append(c)

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
            self.l_cards_on_player_board.append(c)
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
            self.l_cards_on_player_board.append(c)
            self.state.player2.hp += c.opponent_health_change
            self.state.player1.hp += c.my_health_change
            self.state.player1.draw += c.card_draw
            self.state.player1.mana -= c.cost
            self.state.l_guard_creatures_on_player_hand.remove(c)
            self.state.l_cards_on_player_hand.remove(c)
            self.state.right_cover = True
            return

    def use_blue(self, c):
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
        self.state.l_cards_on_player_hand.remove(c)

    def use_green(self, c):
        self.l_cards_on_player_board.sort(key=lambda x: x.cost, reverse=True)
        self.l_turn.append("USE " + str(c.instance_id) + " " + str(self.l_cards_on_player_board[0].instance_id) + ";")
        self.l_cards_on_player_board[0].defense += c.defense
        self.l_cards_on_player_board[0].attack += c.attack
        if c.breakthrough:
            self.l_cards_on_player_board[0].breakthrough = True
        if c.charge:
            self.l_cards_on_player_board[0].charge = True
            if self.l_cards_on_player_board[0].lane == self.state.LANE_LEFT and self.l_cards_on_player_board[0] not in self.state.l_left_cards_can_attack:
                self.state.l_left_cards_can_attack.append(self.l_cards_on_player_board[0])
            elif self.l_cards_on_player_board[0].lane == self.state.LANE_RIGHT and self.l_cards_on_player_board[0] not in self.state.l_right_cards_can_attack:
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
        self.state.l_cards_on_player_hand.remove(c)

    def use_red(self, c):
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
                elif best_coincidence_card.lane == self.state.LANE_RIGHT:
                    if best_coincidence_card in self.state.l_cards_on_right_lane_opponent:
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
                elif c_attack.lane == self.state.LANE_RIGHT:
                    if c_attack in self.state.l_cards_on_right_lane_opponent:
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
        self.state.l_cards_on_player_hand.remove(c)
