from random import shuffle, randint, choice
from board import BoardState
from copy import copy


class Agent():
    def reward(self, reward):
        pass

    def flush(self):
        pass


class VeryStupidAgent(Agent):
    def act(self, board):
        for cell in [1, 7, 3, 5, 8, 0, 6, 2, 4]:
            if cell not in board.x_occupied and cell not in board.o_occupied:
                return cell


class SmartStupidAgent(Agent):
    def act(self, board):
        for cell in [4, 8, 0, 2, 5, 6, 7, 1, 3]:
            if cell not in board.x_occupied and cell not in board.o_occupied:
                return cell


class StupidAgent(Agent):
    def act(self, board):
        for cell in board.all_cells:
            if cell not in board.x_occupied and cell not in board.o_occupied:
                return cell

    def reward(self, reward):
        pass


class RandomAgent(Agent):
    def act(self, board):
        return randint(0, 8)


class AdvancedRandomAgent(Agent):
    def act(self, board):
        all_cells = copy(board.all_cells)
        for cell in board.x_occupied:
            all_cells.remove(cell)
        for cell in board.o_occupied:
            all_cells.remove(cell)
        return choice(all_cells)


class SmartAgent(Agent):
    def act(self, board):
        for winning_combination in BoardState.winning_combinations:
            winning_cell = None
            cells_missing = 2
            for cell in winning_combination:
                if cell in board.x_occupied:
                    cells_missing = cells_missing - 1
                else:
                    winning_cell = cell
            if cells_missing == 0 and winning_cell not in board.o_occupied:
                return winning_cell

            winning_cell = None
            cells_missing = 2
            for cell in winning_combination:
                if cell in board.o_occupied:
                    cells_missing = cells_missing - 1
                else:
                    winning_cell = cell
            if cells_missing == 0 and winning_cell not in board.x_occupied:
                return winning_cell

        for cell in [4, 8, 0, 2, 6, 1, 3, 5, 7]:
            if cell not in board.x_occupied and cell not in board.o_occupied:
                return cell


class RandomizedSmartAgent(Agent):
    def act(self, board):
        for winning_combination in BoardState.winning_combinations:
            winning_cell = None
            cells_missing = 2
            for cell in winning_combination:
                if cell in board.x_occupied:
                    cells_missing = cells_missing - 1
                else:
                    winning_cell = cell
            if cells_missing == 0 and winning_cell not in board.o_occupied:
                return winning_cell

            winning_cell = None
            cells_missing = 2
            for cell in winning_combination:
                if cell in board.o_occupied:
                    cells_missing = cells_missing - 1
                else:
                    winning_cell = cell
            if cells_missing == 0 and winning_cell not in board.x_occupied:
                return winning_cell

        excellent_cell = 4
        good_cells = [8, 0, 2, 6]
        bad_cells = [1, 3, 5, 7]
        shuffle(good_cells)
        shuffle(bad_cells)

        if excellent_cell not in board.x_occupied and excellent_cell not in board.o_occupied:
            return excellent_cell

        for cell in good_cells:
            if cell not in board.x_occupied and cell not in board.o_occupied:
                return cell

        for cell in bad_cells:
            if cell not in board.x_occupied and cell not in board.o_occupied:
                return cell