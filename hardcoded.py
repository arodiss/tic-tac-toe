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
    points_scored += play_set(neural_agent, random_agent)
    points_scored += play_set(neural_agent, very_stupid_agent)
    points_scored += play_set(neural_agent, advanced_random_agent)
    points_scored += play_set(neural_agent, smart_stupid_agent)
    points_scored += play_set(neural_agent, stupid_agent)
    points_scored += play_set(neural_agent, smart_agent)
    points_scored += play_set(neural_agent, randomized_smart_agent)

    print('{}Total points{}: {}'.format(FONT_BOLD + COLOR_GREEN, COLOR_END, points_scored))
    if max_points_scored is None or points_scored > max_points_scored:
        print('This is new best model! Saving it...')
        neural_agent.save()
        max_points_scored = points_scored
    print_separator()
