import numpy as np
import random
from itertools import product

class QLearningAllocationAgent:
    def __init__(self, dc_caps, max_spot=50, initial_lr=0.1, initial_epsilon=0.2, discount=0.5):
        self.dc_caps = dc_caps
        self.max_spot = max_spot
        self.gamma = discount 

        self.initial_lr = initial_lr
        self.lr = initial_lr
        self.min_lr = 0.01
        self.lr_decay = 0.99

        self.initial_epsilon = initial_epsilon
        self.epsilon = initial_epsilon
        self.min_epsilon = 0.01
        self.epsilon_decay = 0.995

        self.step_count = 0

        self.actions = list(product(
            range(dc_caps['sf'] + 1),
            range(dc_caps['ny'] + 1),
            range(dc_caps['tx'] + 1),
            range(0, max_spot + 1, 5)
        ))

        self.q_table = {}
        self.last_state = None
        self.last_action_idx = None
        self.prev_alloc = {'dc': {'sf': 0, 'ny': 0, 'tx': 0}, 'spot': 0}

    def _discretize_state(self, spot_price, revenue_per_ths):
        return (round(spot_price, 2), round(revenue_per_ths, 3))

    def choose_allocation(self, spot_price, revenue_per_ths):
        state = self._discretize_state(spot_price, revenue_per_ths)
        self.last_state = state

        if state not in self.q_table:
            self.q_table[state] = np.zeros(len(self.actions))

        self.step_count += 1

        # Decay learning rate and epsilon
        self.lr = max(self.min_lr, self.initial_lr * self.lr_decay ** self.step_count)
        self.epsilon = max(self.min_epsilon, self.initial_epsilon * self.epsilon_decay ** self.step_count)

        # Epsilon-greedy action selection
        if random.random() < self.epsilon:
            idx = random.randint(0, len(self.actions) - 1)
        else:
            idx = np.argmax(self.q_table[state])

        self.last_action_idx = idx
        alloc = self.actions[idx]
        return {'dc': {'sf': alloc[0], 'ny': alloc[1], 'tx': alloc[2]}, 'spot': alloc[3]}

    def clamp_allocation(self, alloc, max_dc_delta=2, max_spot_delta=10):
        clamped = {'dc': {}, 'spot': alloc['spot']}

        for loc in self.dc_caps:
            prev = self.prev_alloc['dc'][loc]
            desired = alloc['dc'][loc]
            clamped['dc'][loc] = max(0, min(self.dc_caps[loc], prev + max(-max_dc_delta, min(desired - prev, max_dc_delta))))

        prev_spot = self.prev_alloc['spot']
        desired_spot = alloc['spot']
        clamped['spot'] = max(0, min(self.max_spot, prev_spot + max(-max_spot_delta, min(desired_spot - prev_spot, max_spot_delta))))

        # Ensure non-zero action to avoid getting stuck
        if sum(clamped['dc'].values()) + clamped['spot'] == 0:
            clamped['spot'] = 5

        self.prev_alloc = clamped
        return clamped

    def update(self, reward, new_spot_price, new_revenue_per_ths):
        if self.last_state is None or self.last_action_idx is None:
            return

        next_state = self._discretize_state(new_spot_price, new_revenue_per_ths)
        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(len(self.actions))

        best_next_q = np.max(self.q_table[next_state])
        current_q = self.q_table[self.last_state][self.last_action_idx]

        # Q-learning update rule with decaying learning rate
        self.q_table[self.last_state][self.last_action_idx] = current_q + self.lr * (
            reward + self.gamma * best_next_q - current_q
        )

        self.last_state = None
        self.last_action_idx = None
