from board import BoardState
from random import random
from formatting import *


def play_against(agent):
    print('Please notice that it takes approximately a zillion games for agent to become better')
    while True:
        debug = False
        input_debug = input('Do you want to see probability distribution ("thoughts") of AI? y/n:')
        if input_debug == 'y':
            debug = True
            break
        elif input_debug == 'n':
            break

    while True:  # game series
        print_line()
        board = BoardState()
        if random() > 0.5:
            print('You won a toss - place X!')
            while True:  # one game
                board.render()
                x_move = int(input('Your move is... '))
                if not board.is_legal_move(x_move):
                    print('This is illegal move - you {}lost{}!'.format(COLOR_RED, COLOR_END))
                    break
                if board.put_x(x_move):
                    print('Congratulations - you {}won{}!'.format(COLOR_GREEN, COLOR_END))
                    break
                if board.is_over():
                    print('That\'s it - game is over with {}draw{}!'.format(COLOR_YELLOW, COLOR_END))
                    break

                if debug:
                    board.render_distribution(agent.get_distribution(board))
                o_move = agent.act(board)
                if not board.is_legal_move(o_move):
                    print('AI made illegal move - so you {}won{}!'.format(COLOR_GREEN, COLOR_END))
                    break
                if board.put_o(o_move):
                    print('AI finished his combination and you {}lost{}!'.format(COLOR_RED, COLOR_END))
                    break
                if board.is_over():
                    print('That\'s it - game is over with {}draw{}!'.format(COLOR_YELLOW, COLOR_END))
                    break

        else:
            print('You lost a toss - AI will now place X!')
            while True:  # one game
                if debug:
                    board.render_distribution(agent.get_distribution(board))
                x_move = agent.act(board)
                if not board.is_legal_move(x_move):
                    print('AI made illegal move - so you {}won{}!'.format(COLOR_GREEN, COLOR_END))
                    break
                if board.put_x(x_move):
                    print('AI finished his combination and you {}lost{}!'.format(COLOR_RED, COLOR_END))
                    break
                if board.is_over():
                    print('That\'s it - game is over with {}draw{}!'.format(COLOR_YELLOW, COLOR_END))
                    break

                board.render()
                o_move = int(input('Your move is... '))
                if not board.is_legal_move(o_move):
                    print('This is illegal move - you {}lost{}!'.format(COLOR_RED, COLOR_END))
                    break
                if board.put_o(o_move):
                    print('Congratulations - you {}won{}!'.format(COLOR_GREEN, COLOR_END))
                    break
                if board.is_over():
                    print('That\'s it - game is over with {}draw{}!'.format(COLOR_YELLOW, COLOR_END))
                    break