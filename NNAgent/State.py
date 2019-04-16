

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
        self.l_cards_on_player_hand = []         # list of cards on player hand
        self.l_cards_on_left_lane_player = []    # list of cards on the left side of the player board
        self.l_cards_on_left_lane_opponent = []  # list of cards on the left side of the opponent board
        self.l_cards_on_right_lane_player = []   # list of cards on the right side of the player board
        self.l_cards_on_right_lane_opponent = [] # list of cards on the right side of the opponent board

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
            elif c.location == self.LOCATION_PLAYER_SIDE and c.lane == self.LANE_LEFT:
                self.l_cards_on_left_lane_player.append(c)
            elif c.location == self.LOCATION_OPPONENT_SIDE and c.lane == self.LANE_LEFT:
                self.l_cards_on_left_lane_opponent.append(c)
            elif c.location == self.LOCATION_PLAYER_SIDE and c.lane == self.LANE_RIGHT:
                self.l_cards_on_right_lane_player.append(c)
            elif c.location == self.LOCATION_OPPONENT_SIDE and c.lane == self.LANE_RIGHT:
                self.l_cards_on_right_lane_opponent.append(c)

    # ---------------------------------------
    # return true is the game is in the draft phase
    def is_draft_phase(self):
        return self.player1.mana == 0

    # ----------------------------------------------
    # Return the string with state data for NN
    # ----------------------------------------------
    def string_state(self):
        all_string = self.player1.data_string() + ',' + self.player2.data_string()
        for i in range(0, 8):
            all_string += ','
            if i < len(self.l_cards_on_player_hand):
                all_string += str(self.l_cards_on_player_hand[i].card_id)
            else:
                all_string += '0'
        for i in range(0, 3):
            all_string += ','
            if i < len(self.l_cards_on_left_lane_player):
                all_string += self.l_cards_on_player_hand[i].data_string()
            else:
                all_string += '0,0,0,0,0,0,0,0'
        for i in range(0, 3):
            all_string += ','
            if i < len(self.l_cards_on_right_lane_player):
                all_string += self.l_cards_on_player_hand[i].data_string()
            else:
                all_string += '0,0,0,0,0,0,0,0'
        for i in range(0, 3):
            all_string += ','
            if i < len(self.l_cards_on_left_lane_opponent):
                all_string += self.l_cards_on_player_hand[i].data_string()
            else:
                all_string += '0,0,0,0,0,0,0,0'
        for i in range(0, 3):
            all_string += ','
            if i < len(self.l_cards_on_right_lane_opponent):
                all_string += self.l_cards_on_player_hand[i].data_string()
            else:
                all_string += '0,0,0,0,0,0,0,0'
        return all_string
