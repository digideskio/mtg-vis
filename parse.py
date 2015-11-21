import csv
import json
from collections import Counter
from itertools import combinations
from statistics import mean

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

with open('bfz-games.csv') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=games_columns)
    for row in reader:
        game = Game()
        game.cards_played = ",".join(row[None]).split('[')[1:]
        card_count = Counter(game.cards_played)
        game.won = bool(int(row[won]))
        if game.won:
            update(card_count, add_win)
        else:
            update(card_count, add_loss)

def write(filename, declaration, value):
    with open(filename, 'w') as outfile:
        outfile.write(declaration)
        json.dump(value, outfile, indent="")

nodes = [{'id': card.name, 'label': card.name, 'value': win_rate(card),
          'title': str.format("{}<br>{:.0f}%, {} games", card.name,
                              100 * win_rate(card), plays(card))}
         for card in cards_by_name.values()]
write('nodes.js', "var nodes = ", nodes)

edges = [{'from': synergy.card1, 'to': synergy.card2,
          'value': win_rate(synergy),
          'title': str.format("{}<br>{:.0f}%, {} games<br>{}", synergy.card1,
                              100 * win_rate(synergy), plays(synergy),
                              synergy.card2),
          'color': {'opacity': 2 * (win_rate(synergy) - .5)}
         }
         for synergy in synergies_by_card_tuple.values()
         if win_rate(synergy) > .5
         and loss_rate(synergy) < .9 * min(loss_rate(cards_by_name[synergy.card1]), loss_rate(cards_by_name[synergy.card2]))
         and plays(synergy) > .1 * min(plays(cards_by_name[synergy.card1]), plays(cards_by_name[synergy.card2]))
        ]
write('edges.js', "var edges = ", edges)
