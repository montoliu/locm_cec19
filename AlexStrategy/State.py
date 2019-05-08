

# ------------------------------------------------------------
# State information
# ------------------------------------------------------------
class State:
    def __init__(self, player1, player2, opponent_hand, l_opponent_actions, l_cards):
        self.player1 = player1
        self.player2 = player2
        self.opponent_hand = opponent_hand
        self.l_opponent_actions = l_opponent_actions
        self.l_cards = l_cards

        self.LOCATION_IN_HAND = 0
        self.LOCATION_PLAYER_SIDE = 1
        self.LOCATION_OPPONENT_SIDE = -1

        self.LANE_LEFT = 1
        self.LANE_RIGHT = 0

        self.TYPE_CREATURE = 0
        self.TYPE_GREEN = 1
        self.TYPE_RED = 2
        self.TYPE_BLUE = 3

        self.l_actions = []
        self.l_cards_on_player_hand = []  # list of cards on player hand
        self.l_guard_creatures_on_player_hand = []  # list of guard creatures on player hand
        self.l_green_objects_on_player_hand = []  # list of green objects on player hand
        self.l_blue_objects_on_player_hand = []  # list of blue objects on player hand
        self.l_red_objects_on_player_hand = []  # list of red objects on player hand
        self.l_cards_on_left_lane_player = []  # list of cards on the left side of the player board
        self.l_cards_on_left_lane_opponent = []  # list of cards on the left side of the opponent board
        self.l_cards_on_right_lane_player = []  # list of cards on the right side of the player board
        self.l_cards_on_right_lane_opponent = []  # list of cards on the right side of the opponent board
        self.l_left_opponent_cards_guard = []  # list of cards on the right side of the opponent board
        self.l_right_opponent_cards_guard = []  # list of cards on the right side of the opponent board
        self.l_left_opponent_cards_drain = []  # list of cards on the right side of the opponent board
        self.l_right_opponent_cards_drain = []  # list of cards on the right side of the opponent board
        self.l_left_opponent_cards_lethal = []  # list of cards on the right side of the opponent board
        self.l_right_opponent_cards_lethal = []  # list of cards on the right side of the opponent board
        self.l_left_cards_can_attack = []
        self.l_right_cards_can_attack = []

        self.left_cover = False
        self.right_cover = False

        if not self.is_draft_phase():
            self.classify_cards()

    # ---------------------------------------
    # Classify each card in the corresponding list (only if cost <= player mana)
    # Can attack cards on the players lane (already summoned)
    # Can be summoned criatures on the hand
    # Can be used items on the hand
    def classify_cards(self):
        for c in self.l_cards:
            if c.location == self.LOCATION_IN_HAND:
                self.l_cards_on_player_hand.append(c)
                if c.card_type == self.TYPE_CREATURE and c.guard:
                    self.l_guard_creatures_on_player_hand.append(c)
                if c.card_type == self.TYPE_GREEN:
                    self.l_green_objects_on_player_hand.append(c)
                elif c.card_type == self.TYPE_BLUE:
                    self.l_blue_objects_on_player_hand.append(c)
                elif c.card_type == self.TYPE_RED:
                    self.l_red_objects_on_player_hand.append(c)
            elif c.location == self.LOCATION_PLAYER_SIDE and c.lane == self.LANE_LEFT:
                self.l_cards_on_left_lane_player.append(c)
                self.l_left_cards_can_attack.append(c)
                if c.guard:
                    self.left_cover = True
            elif c.location == self.LOCATION_OPPONENT_SIDE and c.lane == self.LANE_LEFT:
                self.l_cards_on_left_lane_opponent.append(c)
                if c.guard:
                    self.l_left_opponent_cards_guard.append(c)
                if c.drain:
                    self.l_left_opponent_cards_drain.append(c)
                if c.lethal:
                    self.l_left_opponent_cards_lethal.append(c)
            elif c.location == self.LOCATION_PLAYER_SIDE and c.lane == self.LANE_RIGHT:
                self.l_cards_on_right_lane_player.append(c)
                self.l_right_cards_can_attack.append(c)
                if c.guard:
                    self.right_cover = True
            elif c.location == self.LOCATION_OPPONENT_SIDE and c.lane == self.LANE_RIGHT:
                self.l_cards_on_right_lane_opponent.append(c)
                if c.guard:
                    self.l_right_opponent_cards_guard.append(c)
                if c.drain:
                    self.l_right_opponent_cards_drain.append(c)
                if c.lethal:
                    self.l_right_opponent_cards_lethal.append(c)

    # ---------------------------------------
    # return true is the game is in the draft phase
    def is_draft_phase(self):
        return self.player1.mana == 0

    def player_cardvalue(self):
        value = 0
        for c in self.l_cards_on_right_lane_player:
            value += c.value()
        for c in self.l_cards_on_left_lane_player:
            value += c.value()
        return value

    def opponent_cardvalue(self):
        value = 0
        for c in self.l_cards_on_right_lane_opponent:
            value += c.value()
        for c in self.l_cards_on_left_lane_opponent:
            value += c.value()
        return value
