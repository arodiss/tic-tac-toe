from formatting import *
from model import NeuralAgent
from environment import play_set
from model import agent_exists, load_user_agent
import intro


print('Please notice that for training to happen agents should be more or less of the same skill')
print('Once one agent dominates the other, training is no longer efficient')
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
adversary = NeuralAgent()

while True:
    play_set(neural_agent, adversary)
    neural_agent.save()
    print_separator()
