import pickle
import random
from collections import defaultdict

from chatbot.flip_seven.models import Action, GameState, PlayerState


# https://en.wikipedia.org/wiki/Q-learning 
class QAgent:
    def __init__(
        self,
        alpha=0.1,
        gamma=0.99,
        epsilon=0.1,
    ):
        self.q_table = defaultdict(lambda: [0.0, 0.0])  # [Q(STOP), Q(TAKE)]
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def state_key(self, player_state: PlayerState):
        # Use a tuple of sorted deck as state key for simplicity
        return tuple(sorted(player_state.deck))

    def select_action(self, player_state: PlayerState):
        key = self.state_key(player_state)
        if random.random() < self.epsilon:
            return random.choice(list(Action))
        q_values = self.q_table[key]
        return Action(q_values.index(max(q_values)))

    def update(self, state, action, reward, next_state):
        key = self.state_key(state)
        next_key = self.state_key(next_state)
        action_idx = int(action)
        best_next = max(self.q_table[next_key])
        td_target = reward + self.gamma * best_next
        td_error = td_target - self.q_table[key][action_idx]
        self.q_table[key][action_idx] += self.alpha * td_error

    def save(self, path):
        with open(path, "wb") as f:
            pickle.dump(dict(self.q_table), f)

    def load(self, path):
        with open(path, "rb") as f:
            self.q_table = defaultdict(lambda: [0.0, 0.0], pickle.load(f))

def q_learning_strategy(
    episodes=10000,
    alpha=0.1,
    gamma=0.99,
    epsilon=0.1,
    verbose=False,
):
    agent = QAgent(alpha=alpha, gamma=gamma, epsilon=epsilon)
    for ep in range(episodes):
        game_state = GameState.initialize_game()
        player_state = PlayerState(deck=[])
        done = False
        while not done:
            state = PlayerState(deck=list(player_state.deck))
            action = agent.select_action(state)
            # Simulate one step
            if action == Action.TAKE:
                if not game_state.deck:
                    reward = state.get_reward()
                    next_state = PlayerState(deck=list(state.deck))
                    done = True
                else:
                    card = game_state.draw_card()
                    next_state = PlayerState(deck=state.deck + [card])
                    reward = next_state.get_reward()
                    if reward == -1:
                        done = True
            else:  # STOP
                reward = state.get_reward()
                next_state = PlayerState(deck=list(state.deck))
                done = True
            agent.update(state, action, reward, next_state)
        if verbose and (ep + 1) % 1000 == 0:
            print(f"Episode {ep+1}/{episodes}")
    return agent

# Example policy function using the learned Q-table
def optimal_policy(agent: QAgent):
    def policy(player_state: PlayerState):
        key = agent.state_key(player_state)
        q_values = agent.q_table[key]
        return Action(q_values.index(max(q_values)))
    return policy    return policy