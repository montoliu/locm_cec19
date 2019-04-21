

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

    # ----------------------------------------------
    # Return the string with player data for NN
    # ----------------------------------------------
    def get_str(self):
        s = str(self.hp) + ',' + str(self.mana) + ',' + str(self.cards_remaining) + ',' + str(self.rune) + ',' + str(self.draw)
        return s
