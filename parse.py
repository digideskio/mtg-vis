import csv
import json
from collections import Counter

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
                          self.name, self.win_rate())

    def win_rate(self):
        if self.wins:
            return self.wins / (self.wins + self.losses)
        else:
            return 0

class Game(object):
    game_id, starting_hand_size, tournament_id, match_id, player, lands_played,
    last_turn, played_first, won, date, constructed_rating, limited_rating,
    match_round, cards_played

    def __init(self):
        super(Game, self).__init__()

cards_by_name = {}
games = []

with open('bfz-cards.csv') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=cards_columns)
    for row in reader:
        cards_by_name[row[name]] = Card(name=row[name],
                                        mana_cost=row[mana_cost],
                                        rarity=row[rarity])

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

with open('bfz-games.csv') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=games_columns)
    for row in reader:
        game = Game()
        games.append(game)
        game.cards_played = ",".join(row[None]).split('[')[1:]
        game.won = bool(int(row[won]))
        for card_name in game.cards_played:
            if game.won:
                cards_by_name[card_name].wins += 1
            else:
                cards_by_name[card_name].losses += 1

with open('nodes.js', 'w') as outfile:
    outfile.write("var nodes = ")
    nodes = [{'id': card.name, 'label': card.name, 'value': card.win_rate()}
             for card in cards_by_name.values()]
    json.dump(nodes, outfile, indent="")
