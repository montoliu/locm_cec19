# This agent select always the first card on the draft phase
# In the battle phase selects randomly the next action to do
import sys
import random


# ------------------------------------------------------------
# Player information
# ------------------------------------------------------------
class Player:
    def __init__(self, hp, mana, cards_remaining, rune, draw):
        self.hp = hp
        self.mana = mana
        self.cards_remaining = cards_remaining  # the number of cards in the player's deck
        self.rune = rune                        # the next remaining rune of a player
        self.draw = draw                        # the additional number of drawn cards


# ------------------------------------------------------------
# Card information
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

        self.l_cards_on_player_hand = []         # list of cards on player hand
        self.l_cards_on_left_lane_player = []    # list of cards on the left side of the player board
        self.l_cards_on_left_lane_opponent = []  # list of cards on the left side of the opponent board
        self.l_cards_on_right_lane_player = []   # list of cards on the right side of the player board
        self.l_cards_on_right_lane_opponent = [] # list of cards on the right side of the opponent board
        self.l_cards_can_attack = []             # list of cards that can attack (criatures on both sides of the board with cost <= player mana)
        self.l_cards_can_be_used = []            # list of cards that can be used (items on the hand with cost <= player mana)
        self.l_cards_can_be_summoned = []        # list of cards that can be summoned (criatures on the hand with cost <= player mana)
        self.classify_cards()

        print("l_cards_on_player_hand: " + str(len(self.l_cards_on_player_hand)), file=sys.stderr)
        print("l_cards_on_left_lane_player: " + str(len(self.l_cards_on_left_lane_player)), file=sys.stderr)
        print("l_cards_on_left_lane_opponent: " + str(len(self.l_cards_on_left_lane_opponent)), file=sys.stderr)
        print("l_cards_on_right_lane_player: " + str(len(self.l_cards_on_right_lane_player)), file=sys.stderr)
        print("l_cards_on_right_lane_opponent: " + str(len(self.l_cards_on_right_lane_opponent)), file=sys.stderr)
        print("l_cards_can_attack: " + str(len(self.l_cards_can_attack)), file=sys.stderr)
        print("l_cards_can_be_used: " + str(len(self.l_cards_can_be_used)), file=sys.stderr)
        print("l_cards_can_be_summoned: " + str(len(self.l_cards_can_be_summoned)), file=sys.stderr)

    # ---------------------------------------
    # Classify each card in the corresponding list (or lists)
    # Can attack cards on the players lane (already summoned)
    # Can be summoned criatures on the hand
    # Can be used items on the hand
    def classify_cards(self):
        for c in self.l_cards:
            if c.location == self.LOCATION_IN_HAND:
                self.l_cards_on_player_hand.append(c)
                if c.cost <= self.player1.mana:
                    if c.card_type == self.TYPE_CREATURE:
                        self.l_cards_can_be_summoned.append(c)
                    else:
                        self.l_cards_can_be_used.append(c)
            elif c.location == self.LOCATION_PLAYER_SIDE and c.lane == self.LANE_LEFT:
                self.l_cards_on_left_lane_player.append(c)
                if c.cost <= self.player1.mana:
                    self.l_cards_can_attack.append(c)
            elif c.location == self.LOCATION_OPPONENT_SIDE and c.lane == self.LANE_LEFT:
                self.l_cards_on_left_lane_opponent.append(c)
            elif c.location == self.LOCATION_PLAYER_SIDE and c.lane == self.LANE_RIGHT:
                self.l_cards_on_right_lane_player.append(c)
                if c.cost <= self.player1.mana:
                    self.l_cards_can_attack.append(c)
            elif c.location == self.LOCATION_OPPONENT_SIDE and c.lane == self.LANE_RIGHT:
                self.l_cards_on_right_lane_opponent.append(c)

    # ---------------------------------------
    # return true is the game is in the draft phase
    def is_draft_phase(self):
        return self.player1.mana == 0


# ------------------------------------------------------------
# Action information
# ------------------------------------------------------------
class Action:
    def __init__(self, action_type):
        self.action_type = action_type   #string
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
        action_str = ""
        if self.action_type == "PASS":
            action_str = "PASS"
        elif self.action_type == "PICK":
            action_str = "PICK " + str(self.id)
        elif self.action_type == "SUMMON":
            action_str = "SUMMON " + str(self.id) + " " + str(self.lane)
        elif self.action_type == "ATTACK":
            action_str = "ATTACK " + str(self.id) + " " + str(self.target_id)
        elif self.action_type == "USE":
            action_str = "USE " + str(self.id) + " " + str(self.target_id)
        return action_str


# ------------------------------------------------------------
# Turn information.
# In a turn more than one action can be performed.
# ------------------------------------------------------------
class Turn:
    def __init__(self):
        self.l_actions = []

    def add_action(self, action):
        self.l_actions.append(action)

    # action are sepparated by ;
    def get_str(self):
        s = self.l_actions[0].get_str()
        for i in range(1,len(self.l_actions)):
            s = s + ";" + self.l_actions[i].get_str()
        return s


# ------------------------------------------------------------
# Agent
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

    # ------------------------------------------------------------
    # read the input and fill corresponfing classes
    # ------------------------------------------------------------
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

    # ----------------------------------------------
    # Select best action to do depending on the pahse
    # ----------------------------------------------
    def act(self):
        if self.state.is_draft_phase():
            best_turn = self.ia_draft()
        else:
            best_turn = self.ia_battle()
        print(best_turn.get_str())

    # ----------------------------------------------
    # This Agent selects always the first card (0)
    # ----------------------------------------------
    def ia_draft(self):
        this_turn = Turn()
        one_action = Action("PICK")
        one_action.set_id(0)
        this_turn.add_action(one_action)
        return this_turn

    # ----------------------------------------------
    # Randomly select the action
    # ----------------------------------------------
    def ia_battle(self):
        this_turn = Turn()

        if len(self.state.l_cards_can_be_summoned) + len(self.state.l_cards_can_be_used)+ len(self.state.l_cards_can_attack) == 0:
            one_action = Action("PASS")
            this_turn.add_action(one_action)
            return this_turn

        # First decision: randomly select if ATTACK or SUMMON/USE
        decision_attack = self.attack_or_other()

        if decision_attack:
            one_action = Action("ATTACK")
            # decide which card will attack and which card or opponent will receive the attack
            which_card_id, which_target_id = self.action_attack()
            one_action.set_id(which_card_id)
            one_action.set_target_id(which_target_id)
            this_turn.add_action(one_action)
        else:
            # Second decision SUMMON or USE
            decision_summon = self.summon_or_use()
            if decision_summon:
                which_card = self.card_to_summon()
                which_lane = self.lane_to_summon()
                if which_lane == -1:
                    one_action = Action("PASS")
                else:
                    one_action = Action("SUMMON")
                    one_action.set_id(which_card.instance_id)
                    one_action.set_lane(which_lane)
                this_turn.add_action(one_action)

                # TODO hay cartas que pueden hacer summon y luego attack
            else:
                which_card = self.card_to_use()
                which_target_id = self.use_item_on(which_card)
                if which_target_id == -2:
                    one_action = Action("PASS")
                else:
                    one_action = Action("USE")
                    one_action.set_id(which_card.instance_id)
                    one_action.set_target_id(which_target_id)
                this_turn.add_action(one_action)

        return this_turn

    # ----------------------------------------------
    # Return True if the decision is to attack, False in other case
    # ----------------------------------------------
    def attack_or_other(self):
        how_many_cards_can_attack = len(self.state.l_cards_can_attack)
        how_many_cards_can_be_summoned = len(self.state.l_cards_can_be_summoned)
        how_many_cards_can_be_used = len(self.state.l_cards_can_be_used)

        print("attack_or_other >> Can attack: " + str(how_many_cards_can_attack), file=sys.stderr)
        print("attack_or_other >> Can be summoned: " + str(how_many_cards_can_be_summoned), file=sys.stderr)
        print("attack_or_other >> Can be used: " + str(how_many_cards_can_be_used), file=sys.stderr)

        if how_many_cards_can_attack == 0:
            return False

        coin = random.randint(1, how_many_cards_can_attack + how_many_cards_can_be_summoned + how_many_cards_can_be_used)
        print("attack_or_other >> coin " + str(coin), file=sys.stderr)

        if coin <= how_many_cards_can_attack:
            return True
        else:
            return False

    # ----------------------------------------------
    # Return True if summon, false if use
    # ----------------------------------------------
    def summon_or_use(self):
        how_many_cards_can_be_summoned = len(self.state.l_cards_can_be_summoned)
        how_many_cards_can_be_used = len(self.state.l_cards_can_be_used)

        if how_many_cards_can_be_summoned == 0:
            return False

        coin = random.randint(1,how_many_cards_can_be_summoned + how_many_cards_can_be_used)
        print("summon_or_use >> coin " + str(coin), file=sys.stderr)

        if coin <= how_many_cards_can_be_summoned:
            return True
        else:
            return False

    # ----------------------------------------------
    # Attack to opponent or to an opponent card on the board
    # ----------------------------------------------
    def action_attack(self):
        which_card = self.select_attacking_card()
        attack_to_card = self.can_attack_opponent_card(which_card)
        if not attack_to_card:
            return which_card.instance_id, -1    # I cannot attack a card, attack to the opponent
        else:
            which_target_id = self.select_target(which_card)
            return which_card.instance_id, which_target_id

    # ----------------------------------------------
    # Select randomly one card to perform the attack
    # It is sure that there is at least one card with cost <= player mana
    # ----------------------------------------------
    def select_attacking_card(self):
        coin = random.randint(0,len(self.state.l_cards_can_attack)-1)
        return self.state.l_cards_can_attack[coin]

    # ----------------------------------------------
    # Return true if the attacking card can attack an opponent card on its lane
    def can_attack_opponent_card(self, attacking_card):
        lane = attacking_card.lane
        if lane == self.LANE_LEFT:
            how_many = len(self.state.l_cards_on_left_lane_opponent)
        else:
            how_many = len(self.state.l_cards_on_right_lane_opponent)

        if how_many == 0:
            return False

        return True

    # ----------------------------------------------
    # Select target to attack. 50% opponent, 50% board
    # ----------------------------------------------
    def select_target(self, attacking_card):
        lane = attacking_card.lane
        if lane == self.LANE_LEFT:
            how_many = len(self.state.l_cards_on_left_lane_opponent)
        else:
            how_many = len(self.state.l_cards_on_right_lane_opponent)

        if how_many == 0:
            return -1

        coin = random.randint(1, 2 * how_many)

        if coin <= how_many:
            return -1
        else:
            # select the opponent card on the board
            l = []
            if lane == self.LANE_LEFT:
                for c in self.state.l_cards_on_left_lane_opponent:
                    l.append(c)
            else:
                for c in self.state.l_cards_on_right_lane_opponent:
                    l.append(c)

            coin = random.randint(0, len(l) - 1)
            return l[coin].instance_id

    # ----------------------------------------------
    # Select randomly a card to summon
    # ----------------------------------------------
    def card_to_summon(self):
        coin = random.randint(0, len(self.state.l_cards_can_be_summoned) - 1)
        return self.state.l_cards_can_be_summoned[coin]

    # ----------------------------------------------
    # Select randomly a card to use. Return lane or -1 if both lanes are full
    # ----------------------------------------------
    def card_to_use(self):
        coin = random.randint(0, len(self.state.l_cards_can_be_used) - 1)
        return self.state.l_cards_can_be_used[coin]

    def lane_to_summon(self):
        howmany_card_left = len(self.state.l_cards_on_left_lane_player)
        howmany_card_right = len(self.state.l_cards_on_right_lane_player)

        if howmany_card_left < 3:
            if howmany_card_right < 3:
                lane = random.randint(0, 1)
            else:
                lane = self.LANE_LEFT
        else:
            if howmany_card_right < 3:
                lane = self.LANE_RIGHT
            else:
                lane = -1
        return lane

    # ----------------------------------------------
    # select the card/player on use item
    # ----------------------------------------------
    def use_item_on(self, which_card):
        if which_card.card_type == self.TYPE_GREEN:
            l = self.state.l_cards_on_right_lane_player + self.state.l_cards_on_right_lane_player
            if len(l) == 0:
                target = -2
            else:
                coin = random.randint(0, len(l) - 1)
                target = l[coin].instance_id
        elif which_card.card_type == self.TYPE_RED:
            l = self.state.l_cards_on_right_lane_opponent + self.state.l_cards_on_right_lane_opponent
            if len(l) == 0:
                target = -2
            else:
                coin = random.randint(0, len(l) - 1)
                target = l[coin].instance_id
        else:
            target = -1

        return target



# -------------------------------------------------------
# Main program.
# At each turn, read input and perform an action
# -------------------------------------------------------
if __name__ == '__main__':
    agent = Agent()
    while True:
        agent.read_input()
        agent.act()



