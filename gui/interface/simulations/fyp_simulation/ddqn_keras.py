# File: ddqn_keras.py

import numpy as np
import tensorflow as tf
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import Adam

class ReplayBuffer:
    def __init__(self, max_size, input_shape, n_actions, discrete=False):
        self.mem_size = max_size
        self.mem_cntr = 0
        self.discrete = discrete
        self.state_memory = np.zeros((self.mem_size, input_shape))
        self.new_state_memory = np.zeros((self.mem_size, input_shape))
        dtype = np.int8 if self.discrete else np.float32
        self.action_memory = np.zeros((self.mem_size, n_actions), dtype=dtype)
        self.reward_memory = np.zeros(self.mem_size)
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.float32)

    def store_transition(self, state, action, reward, state_, done):
        index = self.mem_cntr % self.mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = state_
        if self.discrete:
            actions = np.zeros(self.action_memory.shape[1])
            actions[action] = 1.0
            self.action_memory[index] = actions
        else:
            self.action_memory[index] = action
        self.reward_memory[index] = reward
        self.terminal_memory[index] = 1 - done
        self.mem_cntr += 1

    def sample_buffer(self, batch_size):
        max_mem = min(self.mem_cntr, self.mem_size)
        batch = np.random.choice(max_mem, batch_size)

        states = self.state_memory[batch]
        actions = self.action_memory[batch]
        rewards = self.reward_memory[batch]
        states_ = self.new_state_memory[batch]
        terminal = self.terminal_memory[batch]

        return states, actions, rewards, states_, terminal

class DDQNAgent:
    def __init__(self, alpha, gamma, n_actions, epsilon, batch_size,
                 input_dims, epsilon_dec=0.999995, epsilon_end=0.10,
                 mem_size=25000, fname='ddqn_model.keras', replace_target=25):
        self.action_space = [i for i in range(n_actions)]
        self.n_actions = n_actions
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_dec = epsilon_dec
        self.epsilon_min = epsilon_end
        self.batch_size = batch_size
        self.model_file = fname
        self.replace_target = replace_target
        self.memory = ReplayBuffer(mem_size, input_dims, n_actions, discrete=True)
       
        self.brain_eval = Brain(input_dims, n_actions, batch_size)
        self.brain_target = Brain(input_dims, n_actions, batch_size)

    def remember(self, state, action, reward, new_state, done):
        self.memory.store_transition(state, action, reward, new_state, done)

    def choose_action(self, state):
        state = np.array(state)[np.newaxis, :]
        rand = np.random.random()
        if rand < self.epsilon:
            action = np.random.choice(self.action_space)
        else:
            actions = self.brain_eval.model.predict(state, verbose=0)
            action = np.argmax(actions)
        return action

    def learn(self):
        if self.memory.mem_cntr > self.batch_size:
            state, action, reward, new_state, done = self.memory.sample_buffer(self.batch_size)
            action_indices = np.dot(action, np.array(self.action_space, dtype=np.int8))
            
            q_next = self.brain_target.model.predict(new_state, verbose=0)
            q_eval = self.brain_eval.model.predict(new_state, verbose=0)
            q_pred = self.brain_eval.model.predict(state, verbose=0)

            max_actions = np.argmax(q_eval, axis=1)
            
            q_target = np.copy(q_pred)
            batch_index = np.arange(self.batch_size, dtype=np.int32)
            q_target[batch_index, action_indices] = reward + self.gamma * q_next[batch_index, max_actions.astype(int)] * done

            self.brain_eval.model.fit(state, q_target, verbose=0)
            self.epsilon = max(self.epsilon * self.epsilon_dec, self.epsilon_min)

    def update_network_parameters(self):
        self.brain_target.copy_weights(self.brain_eval)

    def save_model(self):
        self.brain_eval.model.save(self.model_file)  # Save using .keras format
        
    def load_model(self):
        self.brain_eval.model = tf.keras.models.load_model(self.model_file)
        self.brain_target.model = tf.keras.models.load_model(self.model_file)
        if self.epsilon == 0.0:
            self.update_network_parameters()

class Brain:
    def __init__(self, NbrStates, NbrActions, batch_size=256):
        self.NbrStates = NbrStates
        self.NbrActions = NbrActions
        self.batch_size = batch_size
        self.model = self.createModel()
    
    def createModel(self):
        model = Sequential()
        model.add(Dense(256, activation='relu', input_shape=(self.NbrStates,)))
        model.add(Dense(self.NbrActions, activation=tf.keras.activations.softmax))
        model.compile(loss='mse', optimizer=Adam(learning_rate=0.001))
        return model
    
    def copy_weights(self, TrainNet):
        variables1 = self.model.trainable_variables
        variables2 = TrainNet.model.trainable_variables
        for v1, v2 in zip(variables1, variables2):
            v1.assign(v2.numpy())
