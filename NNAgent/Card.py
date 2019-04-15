

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
        self.breakthrough = False
        self.charge = False
        self.drain = False
        self.guard = False
        self.lethal = False
        self.ward = False

        for c in abilities:
            if c == 'B':
                self.breakthrough = True
            elif c == 'C':
                self.charge = True
            elif c == 'D':
                self.drain = True
            elif c == 'G':
                self.guard = True
            elif c == 'L':
                self.lethal = True
            elif c == 'W':
                self.ward = True

    # ----------------------------------------------
    # Return the string with cards on board data for NN
    # ----------------------------------------------
    def data_string(self):
        data_string = str(self.attack) + ',' + str(self.defense)
        for c in self.abilities:
            data_string += ','
            if c != '-':
                data_string += str(1)
            else:
                data_string += str(0)
        return data_string
