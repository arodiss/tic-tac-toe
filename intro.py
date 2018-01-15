from formatting import *
from agents import *
from time import sleep


print_separator()
print('Here randomly initialized neural network plays tic-tac-toe againts set of hardcoded opponents (agents) or against itself')
print('In this version it is possible to make illegal moves (ie try to fill already filled cells). This leads to instant loss')
print('Agents play 98 games vs each other, with switching sides. For each win winner gets +1 point and loser -1 point, so game score is -98 .. +98')
print('Based on game output neural network updates itself, ie gets trained to play better next time')
print('')

print('{}Agents:{}'.format(FONT_BOLD + COLOR_GREEN, COLOR_END))
print('{}{}{} - {}'.format(COLOR_BLUE, RandomAgent.__name__, COLOR_END, "acts totally randomly, including illegal moves"))
print('{}{}{} - {}'.format(COLOR_BLUE, VeryStupidAgent.__name__, COLOR_END, "fills next unoccupied cell in the most-unlikely-to-win sequense (1, 7, 3, 5, 8, 0, 6, 2, 4)"))
print('{}{}{} - {}'.format(COLOR_BLUE, AdvancedRandomAgent.__name__, COLOR_END, "acts randomly, but never does illegal moves"))
print('{}{}{} - {}'.format(COLOR_BLUE, SmartStupidAgent.__name__, COLOR_END, "fills next unoccupied cell in the most-likely-to-win sequense (4, 8, 0, 2, 5, 6, 7, 1, 3)"))
print('{}{}{} - {}'.format(COLOR_BLUE, StupidAgent.__name__, COLOR_END, "fills next unoccupied cell in the most straightforward sequense (0, 1, 2, 3, 4, 5, 6, 7, 8)"))
print('{}{}{} - {}'.format(COLOR_BLUE, SmartAgent.__name__, COLOR_END, "if there is a winning move, does it; if there is a necessary move, does it; otherwise follows most-likely-to-win sequense (4, 8, 0, 2, 5, 6, 7, 1, 3)"))
print('{}{}{} - {}'.format(COLOR_BLUE, RandomizedSmartAgent.__name__, COLOR_END, "same as previous, but with randomization within classes of `corner cells` and `mid-edge cells`"))

print('')
print('{}Legend:{}'.format(FONT_BOLD + COLOR_GREEN, COLOR_END))
print('{}++{} means that {}'.format(COLOR_YELLOW, COLOR_END, "game is won via illegal move"))
print('{}+{} means that {}'.format(COLOR_YELLOW, COLOR_END, "game is won"))
print('{}={} means that {}'.format(COLOR_YELLOW, COLOR_END, "draw (no more free cells left)"))
print('{}-{} means that {}'.format(COLOR_YELLOW, COLOR_END, "game is lost"))
print('{}--{} means that {}'.format(COLOR_YELLOW, COLOR_END, "game is lost via illegal move"))
print('{}Last column{} {}'.format(COLOR_YELLOW, COLOR_END, "displays total points scored versus current opponent"))

print_separator()
input('Press `Enter` to continue...')
