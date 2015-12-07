import csv
import json
from collections import Counter
from itertools import combinations
from math import sqrt
from statistics import mean

from scipy.stats import binom

game_id = 'Game ID'
starting_hand_size = 'Starting hand size'
tournament_id = 'Tournament ID'
match_id = 'Match ID'
player = 'Player'
lands_played = 'Lands played'
last_turn = 'Last turn'
white = 'White'
blue = 'Blue'
black = 'Black'
green = 'Green'
red = 'red'
played_first = 'Played first'
won = 'Won'
date = 'Date'
constructed_rating = 'Constructed rating'
limited_rating = 'Limited rating'
match_round = 'Match round'
cards_played = 'Cards played'
games_columns = (game_id, starting_hand_size, tournament_id, match_id, player,
                 lands_played, last_turn, white, blue, black, green, red,
                 played_first, won, date, constructed_rating, limited_rating,
                 match_round)

cards_columns = (name, mana_cost, rarity) = 'Name', 'Mana cost', 'Rarity'

color_map = {'w': "white",
             'u': "blue",
             'b': "black",
             'r': "red",
             'g': "green",
             'gold': "gold",
             'colorless': "lightgray"}
symbol_map = {'x': "symbol_x.svg",
              'w': "symbol_w.svg",
              'u': "symbol_u.svg",
              'b': "symbol_b.svg",
              'r': "symbol_r.svg",
              'g': "symbol_g.svg",
              'wu': "symbol_w_or_u.svg",
              'ub': "symbol_u_or_b.svg",
              'br': "symbol_b_or_r.svg",
              'rg': "symbol_r_or_g.svg",
              'gw': "symbol_g_or_w.svg",
              'wb': "symbol_w_or_b.svg",
              'ur': "symbol_u_or_r.svg",
              'bg': "symbol_b_or_g.svg",
              'rw': "symbol_r_or_w.svg",
              'gu': "symbol_g_or_u.svg"}

class Card(object):
    wins = 0
    losses = 0

    def __init__(self, name, mana_cost, rarity):
        super(Card, self).__init__()
        self.name = name
        self.mana_cost = mana_cost
        self.rarity = rarity

    def __str__(self):
        return str.format("Card('{}',win_rate()={})",
                          self.name, win_rate(self))
    def color(self):
        colors = 0;
        color = color_map['colorless']
        for c in "wubrg":
            if c in self.mana_cost:
                colors += 1
                color = color_map[c]
        if colors > 1:
            return color_map["gold"]
        else:
            return color

    def group(self):
        colors = 'x'
        for c in "wubrg":
            if c in self.mana_cost:
                colors = c
        for c in ("wu", "ub", "br", "rg", "gw", "wb", "ur", "bg", "rw", "gu"):
            if c in self.mana_cost:
                colors = c
        return colors

    def symbol(self):
        return symbol_map[self.group()]


def plays(element):
    return element.wins + element.losses

def win_rate(element):
    if element.wins:
        return element.wins / plays(element)
    else:
        return 0

def loss_rate(element):
    if element.losses:
        return element.losses / plays(element)
    else:
        return 0

def win_odds(element):
    return (element.wins + 1) / (element.losses + 1)

def lose_odds(element):
    return (element.losses + 1) / (element.wins + 1)

class Game(object):
    game_id, starting_hand_size, tournament_id, match_id, player, lands_played,
    last_turn, played_first, won, date, constructed_rating, limited_rating,
    match_round, cards_played

    def __init__(self):
        super(Game, self).__init__()

class Synergy(object):
    wins = 0
    losses = 0

    def __init__(self, card1, card2):
        super(Synergy, self).__init__()
        self.card1 = card1
        self.card2 = card2

cards_by_name = {}
synergies_by_card_tuple = {}

with open('bfz-cards.csv') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=cards_columns)
    for row in reader:
        cards_by_name[row[name]] = Card(name=row[name],
                                        mana_cost=row[mana_cost],
                                        rarity=row[rarity])

def synergy(card1, card2):
    s = tuple(sorted((card1, card2)))
    synergies_by_card_tuple[s] = synergies_by_card_tuple.get(s, Synergy(*s))
    return synergies_by_card_tuple[s]

def add_win(element):
    element.wins += 1

def add_loss(element):
    element.losses += 1

def update(card_count, function):
    for card_name, amount in card_count.items():
        function(cards_by_name[card_name])
        if amount > 1:
            function(synergy(card_name, card_name))
    for (card1, card2) in combinations(card_count.keys(), 2):
        function(synergy(card1, card2))

games = []

with open('bfz-games.csv') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=games_columns)
    for row in reader:
        game = Game()
        games.append(game)
        game.cards_played = ",".join(row[None]).split('[')[1:]
        card_count = Counter(game.cards_played)
        game.won = bool(int(row[won]))
        if game.won:
            update(card_count, add_win)
        else:
            update(card_count, add_loss)

print(len(games), "games")

def write(filename, declaration, value):
    with open(filename, 'w') as outfile:
        outfile.write(declaration)
        json.dump(value, outfile, indent="")

nodes = [{'id': card.name,
          'value': win_rate(card),
          'group': card.group(),
          'label': str.format("{}", card.name),
          'title': str.format("{}<br>{:.0f}% win rate over {} games",
                              card.name, 100 * win_rate(card), plays(card))}
         for card in cards_by_name.values()]
write('nodes.js', "var nodes = ", nodes)

edges = []

for synergy in synergies_by_card_tuple.values():
    card1 = cards_by_name[synergy.card1]
    card2 = cards_by_name[synergy.card2]

    win_factor = card1.wins * card2.wins
    lose_factor = card1.losses * card2.losses
    combined_win_rate = win_factor / (win_factor + lose_factor)

    golden_mean = .61803398875
    min_plays = 260

    if plays(synergy) > min_plays and win_rate(synergy) > max(golden_mean, combined_win_rate):
        edges.append({'from': synergy.card1,
                      'to': synergy.card2,
                      'value': win_rate(synergy),
                      'length': 95 + 380.0 / (plays(synergy) - min_plays),
                    #   'length': 380 * (1 - win_rate(synergy)),
                      'label': str.format("{:.0f}%", 100 * win_rate(synergy)),
                      'title': str.format("{} + {}<br>{:.0f}% win rate over {} games",
                                          synergy.card1, synergy.card2, 100 * win_rate(synergy), plays(synergy)),
                     })

write('edges.js', "var edges = ", edges)
