import pandas as pd
import numpy as np


# -------------------------------------------------------
# -------------------------------------------------------
class Card():
    def __init__(self, ID, type, cost, attack, defense, keywords, my_health, opponent_health, card_draw):
        self.ID = ID
        self.type = type
        self.cost = cost
        self.attack = attack
        self.defense = defense
        self.keywords = keywords
        self.my_health = my_health
        self.opponent_health = opponent_health
        self.card_draw = card_draw


# -------------------------------------------------------
# -------------------------------------------------------
# NOTA: las cartas que tienen cost == 0 le ponemos como si fuera 1
def EstimateCardValue(list_cards):
    v = np.zeros(len(list_cards))
    i = 0
    for c in list_cards:
        value = c.attack + c.defense + 2*c.my_health - 2*c.opponent_health + 2*c.card_draw
        if 'B' in c.keywords:
            value += 2
        if 'C' in c.keywords:
            value += 2
        if 'D' in c.keywords:
            value += 2
        if 'G' in c.keywords:
            value += 2
        if 'L' in c.keywords:
            value += 2
        if 'W' in c.keywords:
            value += 2

        if c.cost == 0:
            v[i] = value
        else:
            v[i] = value / c.cost
        i += 1
    return v


# -------------------------------------------------------
# -------------------------------------------------------
if __name__ == '__main__':
    cards_data = pd.read_csv("cardlist.txt", delimiter=";", header=None)
    cards_data = cards_data.values

    list_cards = []
    for c in cards_data:
        new_card = Card(c[0], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9])
        list_cards.append(new_card)

    cards_values = EstimateCardValue(list_cards)
    print(cards_values)

    #idx = np.argsort(cards_values)
    #print(idx+1)
    #print(cards_values[idx])
