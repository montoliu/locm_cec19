import random
import numpy as np


# ------------------------------------------------------------
# Draft class
# ------------------------------------------------------------
class Draft:
    def __init__(self):
        self.picked_card_type = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.prefer_card_type = [5, 4, 4, 3, 3, 3, 2, 2, 2, 2]
        self.TYPE_CREATURE = 0
        self.TYPE_GREEN = 1
        self.TYPE_RED = 2
        self.TYPE_BLUE = 3

    def pick_card(self, cards):
        best_card = self.select_bestcard(cards)
        if cards[best_card].card_type == self.TYPE_CREATURE and cards[best_card].cost < 2:
            self.picked_card_type[0] += 1
        elif cards[best_card].card_type == self.TYPE_CREATURE and cards[best_card].cost < 3:
            self.picked_card_type[1] += 1
        elif cards[best_card].card_type == self.TYPE_CREATURE and cards[best_card].cost < 4:
            self.picked_card_type[2] += 1
        elif cards[best_card].card_type == self.TYPE_CREATURE and cards[best_card].cost < 5:
            self.picked_card_type[3] += 1
        elif cards[best_card].card_type == self.TYPE_CREATURE and cards[best_card].cost < 6:
            self.picked_card_type[4] += 1
        elif cards[best_card].card_type == self.TYPE_CREATURE and cards[best_card].cost < 7:
            self.picked_card_type[5] += 1
        elif cards[best_card].card_type == self.TYPE_CREATURE:
            self.picked_card_type[6] += 1
        elif cards[best_card].card_type == self.TYPE_GREEN:
            self.picked_card_type[7] += 1
        elif cards[best_card].card_type == self.TYPE_RED:
            self.picked_card_type[8] += 1
        else:
            self.picked_card_type[9] += 1

        return best_card

    # ------------------------------------------------------------
    # Algorithm to select the best card.
    # First select the card with more abilities.
    # If all cards have the same number of abilities: random
    # It is random, but the types (on picked_card_type) with more gaps are more probables
    def select_bestcard(self, l_cards):
        l_percent = []
        for card in l_cards:
            if card.card_type == self.TYPE_CREATURE:
                if card.cost < 2:
                    p = self.prefer_card_type[0] - self.picked_card_type[0]
                elif card.cost < 3:
                    p = self.prefer_card_type[1] - self.picked_card_type[1]
                elif card.cost < 4:
                    p = self.prefer_card_type[2] - self.picked_card_type[2]
                elif card.cost < 5:
                    p = self.prefer_card_type[3] - self.picked_card_type[3]
                elif card.cost < 6:
                    p = self.prefer_card_type[4] - self.picked_card_type[4]
                elif card.cost < 7:
                    p = self.prefer_card_type[5] - self.picked_card_type[5]
                else:
                    p = self.prefer_card_type[6] - self.picked_card_type[6]
                if card.guard:
                    p += 6
            elif card.card_type == self.TYPE_GREEN:
                p = self.prefer_card_type[7] - self.picked_card_type[7]
            elif card.card_type == self.TYPE_RED:
                p = self.prefer_card_type[8] - self.picked_card_type[8]
            else:
                p = self.prefer_card_type[9] - self.picked_card_type[9]

            if p < 0:
                p = 0
            l_percent.append(p)
        if np.sum(l_percent) == 0:
            n = random.randint(0, 2)
        else:
            result = random.uniform(0, np.sum(l_percent))
            if result <= l_percent[0]:
                n = 0
            elif result <= (l_percent[0] + l_percent[1]):
                n = 1
            else:
                n = 2
        return n
