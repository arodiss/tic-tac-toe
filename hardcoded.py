from agents import *
from formatting import *
from model import NeuralAgent
from environment import play_set
from model import agent_exists, load_user_agent
import intro


if agent_exists():
    while True:
        new_agent = input('Do you want to proceed with your agent from last time? If not, new agent will be trained from scratch (y/n): ')
        if new_agent == 'y':
            neural_agent = load_user_agent()
            break
        elif new_agent == 'n':
            neural_agent = NeuralAgent()
            break
else:
    neural_agent = NeuralAgent()

random_agent = RandomAgent()
very_stupid_agent = VeryStupidAgent()
advanced_random_agent = AdvancedRandomAgent()
smart_stupid_agent = SmartStupidAgent()
stupid_agent = StupidAgent()
smart_agent = SmartAgent()
randomized_smart_agent = RandomizedSmartAgent()

max_points_scored = None
while True:
    points_scored = 0
    fatal_errors = 0
    for adversary in [random_agent, very_stupid_agent, advanced_random_agent, smart_stupid_agent, stupid_agent, smart_agent, randomized_smart_agent]:
        new_points, new_fatals = play_set(neural_agent, adversary)
        points_scored += new_points
        fatal_errors += new_fatals

    print('Total points scored: {}{}{}, number of illegal moves: {}{}{}'.format(
        FONT_BOLD + COLOR_GREEN,
        points_scored,
        COLOR_END,
        FONT_BOLD + COLOR_RED,
        fatal_errors,
        COLOR_END
    ))
    if max_points_scored is None or points_scored > max_points_scored:
        print('This is new best model! Saving it...')
        neural_agent.save()
        max_points_scored = points_scored
    print_separator()
