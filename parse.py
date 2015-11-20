import csv

game_id = 'Game ID'
starting_hand_size = 'Starting hand size'
tournament_id = 'Tournament ID'
match_id = 'Match ID'
player = 'player'
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
                 match_round, cards_played)

cards_columns = (name, mana_cost, rarity) = 'Name', 'Mana cost', 'Rarity'

class Card(object):
    def __init__(self, name, mana_cost, rarity):
        super(Card, self).__init__()
        self.name = name
        self.mana_cost = mana_cost
        self.rarity = rarity

cards = {}

with open('bfz-cards.csv') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=cards_columns)
    for row in reader:
        cards[row[name]] = Card(name=row[name], mana_cost=row[mana_cost],
                                rarity=row[rarity])

with open('bfz-games.csv') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=games_columns)
    row = reader.__next__()
    print(row)
