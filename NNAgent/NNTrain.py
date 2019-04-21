import pandas as pd
import numpy as np
from keras.models import load_model
import drl_memory as drlmemory
import drl_network as drlnetwork


# ---------------------------------------------------------
# ---------------------------------------------------------
class StateNormalizer:
    def __init__(self):
        self.V_MAX = 1

    def normalize(self, v_states):
        v_states_norm = np.zeros(v_states.shape)
        i = 0
        for st in v_states:
            v_states_norm[i, :] = self.normalize_one(st)
            i += 1

        return v_states_norm

    def normalize_one(self, st):
        st_norm = np.array(st.shape)
        return st_norm


# ---------------------------------------------------------
# ---------------------------------------------------------
class NNTrainer:
    def __init__(self, memory_size):
        self.NN_INPUT = 114
        self.NN_HIDDEN = 256
        self.NN_OUTPUT = 2
        self.N_NN_EPOCHS = 3
        self.GAMMA = 0.8
        self.LEARNING_RATE = 0.01

        self.memory = drlmemory.drl_memory(memory_size)
        self.model = self.__build_model()

    # ---------------------------------------------------------
    # ---------------------------------------------------------
    def __build_model(self):
        network = drlnetwork.drl_network(n_input=self.NN_INPUT,
                                         n_hidden=self.NN_HIDDEN,
                                         n_output=self.NN_OUTPUT,
                                         learning_rate=self.LEARNING_RATE)
        return network.model

    # ---------------------------------------------------------
    # ---------------------------------------------------------
    def add_to_memory(self, observation, action, next_observation, reward):
        self.memory.push((observation, next_observation, action, reward))

    # ---------------------------------------------------------
    # ---------------------------------------------------------
    def save_to_disk(self, filename):
        self.model.save(filename)

    # ---------------------------------------------------------
    # ---------------------------------------------------------
    def load_from_disk(self, filename):
        self.model = load_model(filename)

    # ---------------------------------------------------------
    # ---------------------------------------------------------
    def train(self, v_observations, v_next_observations, v_actions, v_rewards):
        v_observations_norm = self.normalize_state(v_observations)
        v_next_observations_norm = self.normalize_state(v_next_observations)

        for observation, next_observation, action, reward in v_observations_norm, v_next_observations_norm, v_actions, v_rewards:
            self.add_to_memory(observation, action, next_observation, reward)

        # Train with all data
        transitions = self.memory.get_all()
        batch_state, batch_next_state, batch_action, batch_reward = (np.array(i) for i in zip(*transitions))

        next_predictions = self.model.predict(batch_next_state)
        max_next_q_values = np.amax(next_predictions, axis=1)

        batch_targets = batch_reward + self.GAMMA * max_next_q_values
        targets_f = self.model.predict(batch_state)

        for i in range(len(batch_action)):
            targets_f[i, batch_action[i]] = batch_targets[i]

        history = self.model.fit(batch_state, targets_f, epochs=self.N_NN_EPOCHS, verbose=0)

    # ---------------------------------------------------------
    # ---------------------------------------------------------
    def normalize_state(self, v_states):
        stn = StateNormalizer()
        return stn.normalize(v_states)


# ---------------------------------------------------------
# ---------------------------------------------------------
if __name__ == "__main__":
    data = pd.read_csv('nn_data.csv', sep=",")
    data = data.values

    v_observations = data[:,0:114]
    v_next_observations = data[:,114:228]
    v_actions = data[:,228]
    v_rewards = data[:,229]

    nn = NNTrainer(data.shape[0])
    nn.train(v_observations, v_next_observations, v_actions, v_rewards)
    nn.save_to_disk("nn.model")

