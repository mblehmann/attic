import json
import random
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *


class RankingEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Item):
            return self.encode_item(obj)
        elif isinstance(obj, Match):
            return self.encode_match(obj)
        elif isinstance(obj, Stats):
            return self.encode_stats(obj)
        elif isinstance(obj, BookMaker):
            return self.encode_bookmaker(obj)
        elif isinstance(obj, Ranker):
            return self.encode_ranker(obj)

        return json.JSONEncoder.default(self, obj)

    @staticmethod
    def encode_item(obj):
        return {
            'type': 'Item',
            'name': obj.name,
        }

    @staticmethod
    def encode_match(obj):
        return {
            'type': 'Match',
            'item0': obj.item0,
            'item1': obj.item1,
            'index': obj.index,
            'winner': obj.winner,
            'loser': obj.loser,
        }

    @staticmethod
    def encode_stats(obj):
        return {
            'type': 'Stats',
            'name': obj.name,
            'wins': obj.wins,
            'losses': obj.losses,
        }

    @staticmethod
    def encode_bookmaker(obj):
        return {
            'type': 'BookMaker',
            'items': obj.items,
            'stats': obj.stats,
            'matrix': obj.matrix,
            'matches': obj.matches,
            'round': obj.round,
        }

    @staticmethod
    def encode_ranker(obj):
        return {
            'type': 'Ranker',
            'stocks': list(obj.stocks.keys()),
            'booker': obj.booker,
            'current_match': obj.current_match,
        }


class RankingDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if 'type' not in obj:
            return obj
        if obj['type'] == 'Item':
            return self.parse_item(obj)
        elif obj['type'] == 'Match':
            return self.parse_match(obj)
        elif obj['type'] == 'Stats':
            return self.parse_stats(obj)
        elif obj['type'] == 'BookMaker':
            return self.parse_bookmaker(obj)
        elif obj['type'] == 'Ranker':
            return self.parse_ranker(obj)
        return obj

    @staticmethod
    def parse_item(obj):
        return Item(**obj)

    @staticmethod
    def parse_match(obj):
        return Match(**obj)

    @staticmethod
    def parse_stats(obj):
        return Stats(**obj)

    @staticmethod
    def parse_bookmaker(obj):
        return BookMaker(**obj)

    @staticmethod
    def parse_ranker(obj):
        return Ranker(**obj)


class Item:

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def __str__(self):
        return self._name


class Match:
    count = 0

    def __init__(self, item0, item1, **kwargs):
        self._item0 = item0
        self._item1 = item1
        if 'index' in kwargs:
            self._index = kwargs.get('index')
            if self._index > Match.count:
                Match.count = self._index + 1
        else:
            self._index = Match.count
            Match.count += 1
        self._winner = kwargs.get('winner', None)
        self._loser = kwargs.get('loser', None)

    @property
    def item0(self):
        return self._item0

    @property
    def item1(self):
        return self._item1

    @property
    def index(self):
        return self._index

    @property
    def winner(self):
        return self._winner

    @property
    def loser(self):
        return self._loser

    @property
    def decided(self):
        return self._winner is not None and self._loser is not None

    def set_result(self, winner, loser):
        self._winner = winner
        self._loser = loser

    def __str__(self):
        return '{} x {} ({})'.format(self._item0, self._item1, self._winner)


class Stats:

    def __init__(self, name, **kwargs):
        self._name = name
        self._wins = kwargs.get('wins', 0)
        self._losses = kwargs.get('losses', 0)

    @property
    def name(self):
        return self._name

    @property
    def wins(self):
        return self._wins

    @property
    def losses(self):
        return self._losses

    @property
    def matches(self):
        return self._wins + self._losses

    @property
    def percentage(self):
        return 100.0 * self._wins / self.matches if self.matches else 0

    def update_wins(self, wins):
        self._wins += wins

    def update_losses(self, losses):
        self._losses += losses

    def __lt__(self, other):
        if self.percentage != other.percentage:
            return self.percentage < other.percentage
        if self.wins != other.wins:
            return self.wins < other.wins
        if self.losses != other.losses:
            return self.losses > other.losses
        return self.name > other.name

    def __str__(self):
        return '{}W/{}L ({:.2f}%)'.format(self._wins, self._losses, self.percentage)


class BookMaker:

    def __init__(self, items, **kwargs):
        self._items = items

        if 'stats' in kwargs:
            self._stats = kwargs.get('stats')
        else:
            self._stats = {}
            for item in self._items:
                self._stats[item] = Stats(item)

        if 'matrix' in kwargs:
            self._matrix = kwargs.get('matrix')
        else:
            self._matrix = {}
            self.create_matrix()

        self._matches = kwargs.get('matches', [])
        self._round = kwargs.get('round', [])

    @property
    def items(self):
        return self._items

    @property
    def stats(self):
        return self._stats

    @property
    def matrix(self):
        return self._matrix

    @property
    def matches(self):
        return self._matches

    @property
    def round(self):
        return self._round

    def create_matrix(self):
        for item in self._items:
            if item not in self._matrix:
                self._matrix[item] = {}
            for other in self._items:
                if other not in self._matrix[item]:
                    self._matrix[item][other] = [0, 0]

    def get_next_match(self):
        if not self._round:
            # self.calculate_round()
            self.generate_season()
        match = self._round.pop(0)
        return match

    def get_previous_match(self, current_match):
        try:
            previous_match = self._matches.pop()
            self._round.insert(0, current_match)
        except IndexError:
            return current_match
        return previous_match

    def generate_season(self):
        pairs = []
        for item0 in self._items:
            for item1 in self._items:
                if item0 != item1 and (item1, item0) not in pairs:
                    pairs.append((item0, item1))

        random.shuffle(pairs)
        for item0, item1 in pairs:
            self._round.append(Match(item0, item1))

    def calculate_round(self):
        candidates = list(self._items)
        assigned = []
        while candidates:
            item0 = random.choice(candidates)
            candidates.remove(item0)
            assigned.append(item0)
            item1 = self.get_opponent(item0, assigned)
            candidates.remove(item1)
            assigned.append(item1)
            self._round.append(Match(item0, item1))

    def get_opponent(self, item0, excluded):
        minimum_matches = min([sum(value) for item, value in self._matrix[item0].items() if item not in excluded])
        candidates = [item for item, value in self._matrix[item0].items()
                      if item not in excluded and sum(value) == minimum_matches]
        return random.choice(candidates)

    def update_result(self, match, revert=False):
        if revert:
            value = -1
        else:
            value = 1
            self._matches.append(match)
        self._stats[match.winner].update_wins(value)
        self._stats[match.loser].update_losses(value)
        self._matrix[match.winner][match.loser][0] += value
        self._matrix[match.loser][match.winner][1] += value

    def get_rank(self):
        return sorted(list(self._stats.items()), key=lambda x: x[1], reverse=True)


class StockData:

    def __init__(self, **kwargs):
        self._name = kwargs.get('name')
        self._market_capitalization = kwargs.get('market_capitalization')
        self._current_price = kwargs.get('current_price')
        self._volume = kwargs.get('volume')
        self._eps = kwargs.get('eps')
        self._eps_10 = kwargs.get('eps_10')
        self._p_e = kwargs.get('p_e')
        self._p_bv = kwargs.get('p_bv')
        self._dividends = kwargs.get('dividends')

    @property
    def data(self):
        return {
            'name': self._name,
            'market_capitalization': self._market_capitalization,
            'current_price': self._current_price,
            'volume': self._volume,
            'eps': self._eps,
            'eps_10': self._eps_10,
            'growth': (self._eps - self._eps_10) / self._eps_10 * 100.0 if self._eps_10 > 0 else '-',
            'p_e': self._p_e,
            'p_bv': self._p_bv,
            'multiplier': self._p_e * self._p_bv,
            'dividends': self._dividends
        }


class Ranker:

    def __init__(self, stocks, **kwargs):
        stock_data = json.load(open('stock_data.json'))
        self._stocks = {}
        for stock in stocks:
            self._stocks[stock] = StockData(**stock_data[stock])
        self._booker = kwargs.get('booker', BookMaker(stocks))
        self._current_match = kwargs.get('current_match', None)

    @property
    def booker(self):
        return self._booker

    @property
    def stocks(self):
        return self._stocks

    @property
    def current_match(self):
        return self._current_match

    def next_match(self):
        self._current_match = self._booker.get_next_match()
        return self._current_match

    def vote(self, winner, loser):
        self._current_match.set_result(winner, loser)
        self._booker.update_result(self._current_match)

    def undo_vote(self):
        self._current_match = self._booker.get_previous_match(self._current_match)
        if self._current_match.decided:
            self._booker.update_result(self._current_match, True)
            self._current_match.set_result(None, None)
        return self._current_match

    def get_stock_data(self, stock):
        return self._stocks[stock].data

    def get_rank(self):
        return self._booker.get_rank()

    def get_matrix(self):
        return self._booker.matrix

    def get_stats(self):
        return self._booker.stats


class UI:

    def __init__(self):
        self._root = Tk()
        self._root.title('Stock Ranking')

        self._stock0 = StringVar()
        self._stock1 = StringVar()
        self._match_index = StringVar()

        self._header_panel = Frame(self._root, padding=10)
        self._match_panel = Frame(self._root, padding=10)
        self._footer_panel = Frame(self._root, padding=10)
        self._side_panel = Frame(self._root, padding=10)

        self._match = Label(self._header_panel, textvariable=self._match_index, font=('', 24), padding=3)

        self._info = Text(self._match_panel, height=12, width=57)
        self._info['state'] = 'disabled'
        self._versus = Label(self._match_panel, text='vs.', font=('', 24), padding=3)
        self._button0 = Button(self._match_panel, textvariable=self._stock0,
                               command=lambda: self.vote(self._stock0.get(), self._stock1.get()), padding=3)
        self._button1 = Button(self._match_panel, textvariable=self._stock1,
                               command=lambda: self.vote(self._stock1.get(), self._stock0.get()), padding=3)

        self._ranking = Button(self._footer_panel, text='Ranking', command=self.show_ranking, padding=3)
        self._undo = Button(self._footer_panel, text='Undo', command=self.undo, padding=3)
        self._matrix = Button(self._footer_panel, text='Matrix', command=self.show_matrix, padding=3)
        self._new = Button(self._footer_panel, text='New', command=self.new, padding=3)
        self._save = Button(self._footer_panel, text='Save', command=self.save, padding=3)
        self._load = Button(self._footer_panel, text='Load', command=self.load, padding=3)

        self.toggle_buttons()

        self._match_log = Text(self._side_panel, height=20, width=27)
        self._match_log['state'] = 'disabled'

        self._match.grid(column=0, row=0)

        self._info.grid(column=0, row=0, columnspan=3)
        self._button0.grid(column=0, row=1)
        self._versus.grid(column=1, row=1)
        self._button1.grid(column=2, row=1)

        self._ranking.grid(column=0, row=0)
        self._undo.grid(column=1, row=0)
        self._matrix.grid(column=2, row=0)
        self._new.grid(column=0, row=1)
        self._save.grid(column=1, row=1)
        self._load.grid(column=2, row=1)

        self._match_log.grid(column=0, row=0)

        self._header_panel.grid(column=0, row=0, sticky=(N, E, S, W))
        self._header_panel.columnconfigure(0, weight=1)

        self._match_panel.grid(column=0, row=1, sticky=(N, E, S, W))
        self._match_panel.columnconfigure(0, weight=1)
        self._match_panel.columnconfigure(2, weight=1)

        self._footer_panel.grid(column=0, row=2, sticky=(N, E, S, W))
        self._footer_panel.columnconfigure(0, weight=1)
        self._footer_panel.columnconfigure(1, weight=1)
        self._footer_panel.columnconfigure(2, weight=1)

        self._side_panel.grid(column=1, row=0, rowspan=3, sticky=(N, E, S, W))
        self._side_panel.columnconfigure(0, weight=1)

        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(1, weight=1)

        self._root.bind('<Left>', lambda _: self._button0.invoke())
        self._root.bind('<Right>', lambda _: self._button1.invoke())

        self._file = None
        self._ranker = None

    def toggle_buttons(self, disabled=True):
        state = 'disabled' if disabled else '!disabled'
        for button in [self._button0, self._button1, self._ranking, self._undo, self._matrix, self._save]:
            button.state([state])

    def generate_next_match(self):
        match = self._ranker.next_match()
        self.display_match(match)

    def display_match(self, match):
        if match.index % 5 == 0:
            self.save()
        self._stock0.set(match.item0)
        self._stock1.set(match.item1)
        self._match_index.set('Match #{}'.format(match.index))
        self.populate_match_info(match)

    def populate_match_info(self, match):
        self._info['state'] = 'normal'
        self._info.delete('1.0', END)
        item0_data = self._ranker.get_stock_data(match.item0)
        item1_data = self._ranker.get_stock_data(match.item1)
        lines = [
            '{:^25} {:^24} {:^8}'.format('metric', match.item0, match.item1),
            '{:-<58}'.format('')
        ]
        for metric in ['market_capitalization', 'current_price', 'volume', 'eps', 'eps_10', 'growth', 'p_e', 'p_bv',
                       'multiplier', 'dividends']:
            line = [
                '{:25}'.format(metric),
                self.format_stock_data(item0_data[metric]),
                self.format_stock_data(item1_data[metric]),
            ]
            lines.append(' '.join(line))
        self._info.insert('1.0', '\n'.join(lines))
        self._info['state'] = 'disabled'

    def append_log(self, match):
        num_entries = int(self._match_log.index('end - 1 line').split('.')[0])
        self._match_log['state'] = 'normal'
        if num_entries >= 20:
            self._match_log.delete(1.0, 2.0)
        if self._match_log.index('end - 1c') != '1.0':
            self._match_log.insert(END, '\n')
        self._match_log.insert(END, '{}'.format(str(match)))
        self._match_log['state'] = 'disabled'

    def remove_log(self):
        last_line = self._match_log.index('end - 1 line')
        self._match_log['state'] = 'normal'
        self._match_log.delete(last_line, END)
        self._match_log['state'] = 'disabled'

    @staticmethod
    def format_stock_data(data):
        if isinstance(data, int):
            return '{:>15,}'.format(data)
        elif isinstance(data, float):
            return '{:>15,.2f}'.format(data)
        else:
            return '{:>15}'.format(data)

    def vote(self, winner, loser):
        self._ranker.vote(winner, loser)
        self.append_log(self._ranker.current_match)
        self.generate_next_match()

    def undo(self):
        match = self._ranker.undo_vote()
        self.remove_log()
        self.display_match(match)

    def show_ranking(self):
        ranking_window = Toplevel(self._root)
        ranking_window.transient(self._root)
        ranking_window.title = 'Ranking'

        ranking_panel = Frame(ranking_window, padding=10)
        Label(ranking_panel, text='Position', padding=3).grid(column=0, row=0)
        Label(ranking_panel, text='Stock', padding=3).grid(column=1, row=0)
        Label(ranking_panel, text='Wins', padding=3).grid(column=2, row=0)
        Label(ranking_panel, text='Losses', padding=3).grid(column=3, row=0)
        Label(ranking_panel, text='Win %', padding=3).grid(column=4, row=0)

        for index, (stock, stats) in enumerate(self._ranker.get_rank()):
            Label(ranking_panel, text='{}'.format(index + 1), padding=3).grid(column=0, row=index + 1)
            Label(ranking_panel, text=stock, padding=3).grid(column=1, row=index + 1)
            Label(ranking_panel, text='{}'.format(stats.wins), padding=3).grid(column=2, row=index + 1)
            Label(ranking_panel, text='{}'.format(stats.losses), padding=3).grid(column=3, row=index + 1)
            Label(ranking_panel, text='{:.2f}'.format(stats.percentage), padding=3).grid(column=4, row=index + 1)
        ranking_panel.grid(column=0, row=0, sticky=(N, E, S, W))

    def show_matrix(self):
        matrix_window = Toplevel(self._root)
        matrix_window.transient(self._root)
        matrix_window.title = 'Matrix'
        matrix_data = self._ranker.get_matrix()
        stats_data = self._ranker.get_stats()

        matrix_panel = Frame(matrix_window, padding=10)
        Label(matrix_panel, text='Total Win %', padding=3).grid(column=len(stats_data) + 2, row=0)
        for i, (stock, matches) in enumerate(matrix_data.items()):
            Label(matrix_panel, text=stock, padding=3).grid(column=i + 1, row=0)
            Label(matrix_panel, text=stock, padding=3).grid(column=0, row=i + 1)
            Label(matrix_panel, text='{:.2f}'.format(stats_data[stock].percentage),
                  padding=3).grid(column=len(stats_data) + 2, row=i + 1)
            for j, (other, count) in enumerate(matches.items()):
                cell = '{:.2f}'.format(100.0 * count[0] / (count[0] + count[1])) if count[0] + count[1] > 0 else '-'
                Label(matrix_panel, text=cell, padding=3).grid(column=j + 1, row=i + 1)

        matrix_panel.grid(column=0, row=0, sticky=(N, E, S, W))

    def new(self):
        self._ranker = Ranker(['ANDR.VI', 'BG.VI', 'CAI.VI', 'EBS.VI', 'EVN.VI', 'MMK.VI',
                               'POST.VI', 'OMV.VI', 'RBI.VI', 'STR.VI', 'UQA.VI', 'VIG.VI'])
        # ['ANDR.VI', 'ATS.VI', 'BG.VI', 'CAI.VI', 'DOC.VI', 'EBS.VI', 'EVN.VI', 'IIA.VI',
        # 'LNZ.VI', 'MMK.VI', 'POST.VI', 'OMV.VI', 'RBI.VI', 'SPI.VI', 'SBO.VI', 'STR.VI',
        # 'UBS.VI', 'UQA.VI', 'VER.VI', 'VIG.VI', 'VOE.VI', 'WIE.VI']
        Match.count = 0
        self.generate_next_match()
        self.toggle_buttons(False)

    def save(self):
        if self._file is None:
            while not self._file:
                self._file = filedialog.asksaveasfilename()
        json.dump(self._ranker, open(self._file, 'w'), cls=RankingEncoder, indent=4)

    def load(self):
        selected_file = filedialog.askopenfilename()
        if selected_file:
            self._file = selected_file
            self._ranker = json.load(open(self._file), cls=RankingDecoder)
            self.display_match(self._ranker.current_match)
            self.toggle_buttons(False)

    def run(self):
        self._root.mainloop()


if __name__ == '__main__':
    app = UI()
    app.run()
