from random import random
from pathlib import Path
import numpy as np
from keras.models import Sequential, save_model, load_model
from keras.layers import Dense
from keras.optimizers import Adam


USER_MODEL_FILE_NAME = 'pretrained.h5'
VENDOR_MODEL_FILE_NAME = 'vendor.h5'


def agent_exists():
    return Path(USER_MODEL_FILE_NAME).is_file()


def load_user_agent():
    return NeuralAgent.from_model(load_model(USER_MODEL_FILE_NAME))


def load_vendor_agent():
    return NeuralAgent.from_model(load_model(VENDOR_MODEL_FILE_NAME))


def vectorize_board(board):
    vectorized = []
    for cell in board.all_cells:
        # clumsy redundant inconsistent representation, but works
        if cell in board.x_occupied:
            vectorized.append(1)
        else:
            vectorized.append(0)
        if cell in board.o_occupied:
            vectorized.append(1)
        else:
            vectorized.append(0)
    return np.array(vectorized)


class NeuralAgent:
    num_inputs = 18
    num_hidden_1 = 100
    num_hidden_2 = 80
    num_hidden_3 = 60
    num_outputs = 9
    reward_discount_rate = .9
    learning_rate = 1e-4

    def __init__(self):
        self.model = Sequential()
        self.model.add(Dense(self.num_hidden_1, activation='relu', input_shape=(self.num_inputs, )))
        self.model.add(Dense(self.num_hidden_2, activation='relu'))
        self.model.add(Dense(self.num_hidden_3, activation='relu'))
        self.model.add(Dense(self.num_outputs, activation='softmax'))
        self.model.compile(
            loss='categorical_crossentropy',
            optimizer=Adam(lr=self.learning_rate)
        )
        self._reset_history()

    @classmethod
    def from_model(cls, model):
        agent = NeuralAgent()
        agent.model = model
        return agent

    def get_distribution(self, board):
        return self.model.predict(np.array([vectorize_board(board)]))[0]

    def act(self, board):
        action_input = vectorize_board(board)
        probabilities = self.model.predict(np.array([action_input]))[0]
        selected_cell = NeuralAgent.sample_cell(probabilities)
        selected_cell_one_hot = np.zeros((self.num_outputs, ))
        selected_cell_one_hot[selected_cell] = 1

        self.history[-1].append({
            'input': action_input,
            'output': probabilities,
            'cell_one_hot': selected_cell_one_hot
        })

        return selected_cell

    def reward(self, reward):
        per_action_rewards = self.get_per_action_rewards(reward)
        for index, reward in enumerate(per_action_rewards):
            self.history[-1][index]['reward'] = reward
        self.history.append([])

    def get_per_action_rewards(self, final_reward):
        per_action_rewards = np.zeros((len(self.history[-1]),))
        current_reward = final_reward
        for index, value in enumerate(per_action_rewards):
            per_action_rewards[index] = current_reward
            current_reward *= NeuralAgent.reward_discount_rate
        per_action_rewards = list(reversed(per_action_rewards))

        return per_action_rewards

    def _reset_history(self):
        self.history = [[]]

    @staticmethod
    def sample_cell(cell_probabilities):
        cell = None
        sample = random()
        for cell, probability in enumerate(cell_probabilities):
            if probability >= sample:
                break
            sample = sample - probability
        return cell

    def flush(self):
        all_rewards = []
        for game in self.history:
            for action in game:
                all_rewards.append(action['reward'])
        mean_reward = np.mean(all_rewards)
        std_rewards = np.std(all_rewards)
        if std_rewards == 0:
            std_rewards = 1

        train_x = []
        train_y = []
        for game in self.history:
            for action in game:
                action_input = action['input']
                action_output = action['output']
                cell_one_hot = action['cell_one_hot']
                reward = (action['reward'] - mean_reward) / std_rewards
                train_x.append(action_input)
                train_y.append((cell_one_hot - action_output) * reward)
        self.model.fit(np.array(train_x), np.array(train_y), verbose=False, epochs=1)
        self._reset_history()

    def save(self):
        save_model(self.model, USER_MODEL_FILE_NAME)