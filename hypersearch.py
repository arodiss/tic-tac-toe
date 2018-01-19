import csv
from random import uniform
from keras.models import Sequential
from keras.optimizers import Adam
from keras.layers import Dense, Dropout
from environment import play_set
from model import NeuralAgent
from agents import *


iterations_per_setting = 5
min_pretraining_rounds_1 = 0
max_pretraining_rounds_1 = 100
min_pretraining_rounds_2 = 0
max_pretraining_rounds_2 = 100
max_rounds_wo_improvement = 50
min_lr_pow = -3.8
max_lr_pow = -3.3
min_discount_rate = 0.7
max_discount_rate = 0.9
min_h1 = 500
max_h1 = 1500
min_h2 = 170
max_h2 = 350
min_h3 = 170
max_h3 = 270
min_d1 = 0.05
max_d1 = 0.1
min_d2 = 0.2
max_d2 = 0.25
min_d3 = 0.2
max_d3 = 0.25


def sample_config():
    return {
        'lr_pow': uniform(min_lr_pow, max_lr_pow),
        'discount_rate': uniform(min_discount_rate, max_discount_rate),
        'pretraining_rounds_1': int(uniform(min_pretraining_rounds_1, max_pretraining_rounds_1)),
        'pretraining_rounds_2': int(uniform(min_pretraining_rounds_2, max_pretraining_rounds_2)),
        'h1': int(uniform(min_h1, max_h1)),
        'h2': int(uniform(min_h2, max_h2)),
        'h3': int(uniform(min_h3, max_h3)),
        'd1': uniform(min_d1, max_d1),
        'd2': uniform(min_d2, max_d2),
        'd3': uniform(min_d3, max_d3),
    }


def create_agent(config):
    NeuralAgent.reward_discount_rate = config['discount_rate']
    NeuralAgent.learning_rate = pow(10, config['lr_pow'])
    model = Sequential()
    model.add(Dense(config['h1'], activation='relu', input_shape=(NeuralAgent.num_inputs,)))
    model.add(Dropout(config['d1']))
    model.add(Dense(config['h2'], activation='relu'))
    model.add(Dropout(config['d2']))
    model.add(Dense(config['h3'], activation='relu'))
    model.add(Dropout(config['d3']))
    model.add(Dense(NeuralAgent.num_outputs, activation='softmax'))
    model.compile(
        loss='categorical_crossentropy',
        optimizer=Adam(lr=pow(10, config['lr_pow']))
    )
    return NeuralAgent.from_model(model)


def save_result(config, points, fatals, best_iteration_index):
    with open('hypersearch.csv', 'a+') as fh:
        writer = csv.writer(fh)
        writer.writerow([
            config['lr_pow'],
            config['pretraining_rounds_1'],
            config['pretraining_rounds_2'],
            config['discount_rate'],
            config['h1'],
            config['h2'],
            config['h3'],
            config['d1'],
            config['d2'],
            config['d3'],
            points,
            fatals,
            best_iteration_index
        ])


random_agent = RandomAgent()
advanced_random_agent = AdvancedRandomAgent()
randomized_smart_agent = RandomizedSmartAgent()
samples_processed = 0
while True:
    config = sample_config()
    total_points = 0
    fatal_errors = 0
    best_round_indices = []
    for i in range(0, iterations_per_setting):
        agent = create_agent(config)
        for j in range(0, config['pretraining_rounds_1']):
            play_set(agent, random_agent, False)
        for k in range(0, config['pretraining_rounds_2']):
            play_set(agent, advanced_random_agent, False)
        best_round_points = None
        best_round_fatals = None
        best_round_index = None
        rounds_wo_improvement = 0
        round_index = 0
        while True:
            round_index += 1
            current_round_points = 0
            current_round_fatals = 0
            for adversary in [randomized_smart_agent, randomized_smart_agent, randomized_smart_agent]:
                new_points, new_fatals = play_set(agent, adversary, False)
                current_round_points += new_points
                current_round_fatals += new_fatals
            if best_round_points is None or current_round_points > best_round_points:
                best_round_points = current_round_points
                best_round_fatals = current_round_fatals
                best_round_index = str(round_index)
                rounds_wo_improvement = 0
            else:
                rounds_wo_improvement += 1
                if rounds_wo_improvement > max_rounds_wo_improvement:
                    break
        total_points += best_round_points
        fatal_errors += best_round_fatals
        best_round_indices.append(best_round_index)
        print('    ... completed iteration {} out of {}, scored {}'.format(i+1, iterations_per_setting, best_round_points))
    save_result(config, total_points, fatal_errors, '-'.join(best_round_indices))
    samples_processed += 1
    print('Finished sample #{}, total score {}'.format(samples_processed, total_points,))
