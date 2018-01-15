from formatting import *
from copy import copy


# board markup is like this:
# 0 | 1 | 2
# 3 | 4 | 5
# 6 | 7 | 8


class BoardState:
    winning_combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]

    def __init__(self):
        self.all_cells = list(range(0, 9))
        self.x_occupied = []
        self.o_occupied = []

    def render(self):
        print('')
        print('Current board state:')
        print(' {} | {} | {}'.format(self._get_symbol(0), self._get_symbol(1), self._get_symbol(2)))
        print(' {} | {} | {}'.format(self._get_symbol(3), self._get_symbol(4), self._get_symbol(5)))
        print(' {} | {} | {}'.format(self._get_symbol(6), self._get_symbol(7), self._get_symbol(8)))
        print('')

    def render_distribution(self, distribution):
        print('')
        print('Probabilities of picking cells by AI:')
        print(' {} | {} | {}'.format(self._format_distribution(0, distribution[0]), self._format_distribution(1, distribution[1]), self._format_distribution(2, distribution[2])))
        print(' {} | {} | {}'.format(self._format_distribution(3, distribution[3]), self._format_distribution(4, distribution[4]), self._format_distribution(5, distribution[5])))
        print(' {} | {} | {}'.format(self._format_distribution(6, distribution[6]), self._format_distribution(7, distribution[7]), self._format_distribution(8, distribution[8])))
        print('')

    def is_legal_move(self, cell_index):
        return cell_index in self.all_cells and cell_index not in self.x_occupied and cell_index not in self.o_occupied

    def put_x(self, cell_index):
        self.x_occupied.append(cell_index)
        return self._is_winning_combination(self.x_occupied)

    def put_o(self, cell_index):
        self.o_occupied.append(cell_index)
        return self._is_winning_combination(self.o_occupied)

    def is_over(self):
        return len(self.x_occupied) + len(self.o_occupied) == len(self.all_cells)

    @staticmethod
    def _is_winning_combination(occupied):
        for winning_combination in BoardState.winning_combinations:
            if len([i for i in occupied if i in winning_combination]) == 3:
                return True
        return False

    def _get_symbol(self, cell_index):
        return 'x' if cell_index in self.x_occupied else 'o' if cell_index in self.o_occupied else ' '

    def _format_distribution(self, cell, raw_value):
        value = str(int(raw_value * 100) / 100).ljust(4, '0')
        if cell in self.x_occupied or cell in self.o_occupied:
            return "{}{}{}".format(COLOR_RED, value, COLOR_END)
        x = copy(self.x_occupied)
        o = copy(self.o_occupied)
        x.append(cell)
        o.append(cell)
        if self._is_winning_combination(x) or self._is_winning_combination(o):
            return "{}{}{}".format(COLOR_GREEN, value, COLOR_END)
        return value
