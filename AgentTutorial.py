import sys


# ------------------------------------------------------------
# ------------------------------------------------------------
class Player:
    def __init__(self, hp, mana, cards_remaining, rune, draw):
        self.hp = hp
        self.mana = mana
        self.cards_remaining = cards_remaining  # the number of cards in the player's deck
        self.rune = rune                        # the next remaining rune of a player
        self.draw = draw                        # the additional number of drawn cards


# ------------------------------------------------------------
# ------------------------------------------------------------
class State:
    def __init__(self, player1, player2, opponent_hand, l_opponent_actions, l_cards):
        self.player1 = player1
        self.player2 = player2
        self.opponent_hand =  opponent_hand
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

    def is_draft_phase(self):
        return self.player1.mana == 0

    def is_full_lane(self, n_lane):
        n = 0
        for c in self.l_cards:
            if c.location == self.LOCATION_PLAYER_SIDE and c.lane == n_lane:
                n += 1
        return n == 3


# ------------------------------------------------------------
# ------------------------------------------------------------
class Card:
    def __init__(self, card_id, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw, lane):
        self.card_id = card_id
        self.instance_id = instance_id
        self.location = location
        self.card_type = card_type
        self.cost = cost
        self.attack = attack
        self.defense = defense
        self.abilities = abilities
        self.my_health_change = my_health_change
        self.opponent_health_change = opponent_health_change
        self.card_draw = card_draw
        self.lane = lane


# ------------------------------------------------------------
# ------------------------------------------------------------
class Action:
    def __init__(self, action_type):
        self.action_type =  action_type   #string
        self.id = None
        self.target_id = None
        self.lane = None

    def set_id(self, id):
        self.id = id

    def set_target_id(self, target_id):
        self.target_id = target_id

    def set_lane(self, lane):
        self.lane = lane

    def get_str(self):
        if self.action_type == "PASS":
            return "PASS"
        elif self.action_type == "PICK":
            return "PICK " + str(self.id)
        elif self.action_type == "SUMMON":
            return "SUMMON " + str(self.id) + " " + str(self.lane)
        elif self.action_type == "ATTACK":
            return "ATTACK " + str(self.id) + " " + str(self.target_id)
        elif self.action_type == "USE":
            return "USE " + str(self.id) + " " + str(self.target_id)


# ------------------------------------------------------------
# ------------------------------------------------------------
class Turn:
    def __init__(self):
        self.l_actions = []

    def add_action(self, action):
        self.l_actions.append(action)

    def get_str(self):
        s = self.l_actions[0].get_str()
        for i in range(1,len(self.l_actions)):
            s = s + ";" + self.l_actions[i].get_str()
        return s


# ------------------------------------------------------------
# ------------------------------------------------------------
class Agent():
    def __init__(self):
        self.state = None
        self.LOCATION_IN_HAND = 0
        self.LOCATION_PLAYER_SIDE = 1
        self.LOCATION_OPPONENT_SIDE = -1

        self.LANE_LEFT = 1
        self.LANE_RIGHT = 0

        self.TYPE_CREATURE = 0
        self.TYPE_GREEN = 1
        self.TYPE_RED = 2
        self.TYPE_BLUE = 3

    def read_input(self):
        player_health1, player_mana1, player_deck1, player_rune1, player_draw1 = [int(j) for j in input().split()]
        player_health2, player_mana2, player_deck2, player_rune2, player_draw2 = [int(j) for j in input().split()]

        opponent_hand, opponent_actions = [int(i) for i in input().split()]
        l_opponent_actions = []
        for i in range(opponent_actions):
            card_number_and_action = input()
            l_opponent_actions.append(card_number_and_action)

        card_count = int(input())
        l_cards = []
        for i in range(card_count):
            card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw, lane = input().split()
            one_card = Card(int(card_number), int(instance_id), int(location), int(card_type), int(cost), int(attack),
                        int(defense), abilities, (my_health_change), int(opponent_health_change), int(card_draw), int(lane))
            l_cards.append(one_card)

        player1 = Player(player_health1, player_mana1, player_deck1, player_rune1, player_draw1)
        player2 = Player(player_health2, player_mana2, player_deck2, player_rune2, player_draw2)
        self.state = State(player1, player2, opponent_hand, l_opponent_actions, l_cards)

    def act(self):
        if self.state.is_draft_phase():
            best_turn = self.ia_draft()
        else:
            best_turn = self.ia_battle()
        print(best_turn.get_str())

    def ia_draft(self):
        this_turn = Turn()
        one_action = Action("PICK")
        one_action.set_id(0)
        this_turn.add_action(one_action)
        return this_turn

    def ia_battle(self):
        this_turn = Turn()

        # Buscamos la mejor criatura en nuestro lado con mana ok para atacar al oponente
        best_card_instance_id = -1
        best_score = -1
        for c in self.state.l_cards:
            if c.location == self.LOCATION_PLAYER_SIDE and c.cost <= self.state.player1.mana and c.card_type == self.TYPE_CREATURE:
                score = c.cost
                if score >= best_score:
                    best_score = score
                    best_card_instance_id = c.instance_id

        if best_card_instance_id != -1:
            one_action = Action("ATTACK")
            one_action.set_id(best_card_instance_id)
            one_action.set_target_id(-1)
            this_turn.add_action(one_action)
            return this_turn

        # Seleccionamos a una criatura que este en nuestra mano y con mana OK para summon
        best_score = 0
        best_card_instance_id = -1
        for c in self.state.l_cards:
            if c.location == self.LOCATION_IN_HAND and c.cost <= self.state.player1.mana and c.card_type == self.TYPE_CREATURE:
                score = c.cost
                if score >= best_score:
                    best_score = score
                    best_card_instance_id = c.instance_id

        if best_card_instance_id != -1:
            one_action = Action("SUMMON")
            one_action.set_id(best_card_instance_id)
            if self.state.is_full_lane(self.LANE_LEFT):
                one_action.set_lane(self.LANE_LEFT)
            else:
                one_action.set_lane(self.LANE_RIGHT)
            this_turn.add_action(one_action)
            return this_turn

        # si no existe alguna PASS.
        one_action = Action("PASS")
        this_turn.add_action(one_action)
        return this_turn

# -------------------------------------------------------
# -------------------------------------------------------
if __name__ == '__main__':
    agent = Agent()
    while True:
        agent.read_input()
        agent.act()



