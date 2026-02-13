import pickle
import random
from itertools import combinations
from typing import Dict, Tuple

from chatbot.flip_seven.game import create_valide_player_state, one_step
from chatbot.flip_seven.models import Action, GameState, PlayerState, QTable


class QLearningAgent:
    def __init__(
        self,
        alpha: float = 0.1,
        gamma: float = 0.9,
        epsilon: float = 0.1,
        max_cards: int = 3,
        max_value: int = 13,
    ):
        self.max_cards = max_cards
        self.max_value = max_value
        self.q_table: QTable = self._init_q_table()
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def _init_q_table(self) -> QTable:
        values: Dict[Tuple, Dict[Action, float]] = {
            (): {Action.TAKE: 0.0, Action.STOP: 0.0}
        }
        card_range = range(0, self.max_value + 1)
        for num_cards in range(1, self.max_cards + 1):
            for state_tuple in combinations(card_range, num_cards):
                values[state_tuple] = {Action.TAKE: 0.0, Action.STOP: 0.0}
        return QTable(values=values, possible_actions=list(Action))

    def selection_action(self, state: PlayerState) -> Action:
        state_tuple: Tuple[int, ...] = state.get_tuple()
        if state_tuple not in self.q_table.values:
            raise ValueError(f"State {state_tuple} not found in Q-table.")

        # Exploration
        if random.random() < self.epsilon:
            return random.choice(list(Action))
        # Exploitation
        return self.q_table.get_best_action(state_tuple)

    # def get_q_value(self, state: PlayerState, action: Action) -> float:
    #     state_tuple: Tuple[int, ...] = state.get_tuple()
    #     if state_tuple not in self.q_table.values:
    #         raise ValueError(f"State {state_tuple} not found in Q-table.")
    #         # return None
    #     return self.q_table.values[state_tuple][action]

    # def set_q_value(self, state: PlayerState, action: Action, value: float) -> None:
    #     state_tuple: Tuple[int, ...] = state.get_tuple()
    #     if state_tuple not in self.q_table.values:
    #         raise ValueError(f"State {state_tuple} not found in Q-table.")
    #         # return None
    #     self.q_table.values[state_tuple][action] = value

    def update_q_value(
        self,
        state: PlayerState,
        action: Action,
        reward: float,
        state_next: PlayerState,
        done: bool,
    ) -> None:
        # Get the current Q-value for the state-action pair
        current_q: float = self.q_table.get_q_value(state, action)
        if done:
            next_max_q = 0.0
        else:
            next_max_q: float = max(
                self.q_table.get_q_value(state_next, a) for a in Action
            )
        new_q: float = current_q + self.alpha * (
            reward + self.gamma * next_max_q - current_q
        )
        self.q_table.set_q_value(state, action, new_q)

    # Utils functions to save and load the Q-table
    def save_q_table(self, filepath: str) -> None:
        """Save the Q-table to a file using pickle."""
        with open(filepath, "wb") as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, filepath: str) -> None:
        """Load the Q-table from a file using pickle."""
        with open(filepath, "rb") as f:
            self.q_table = pickle.load(f)


def q_learning_strategy(
    episodes: int,
    alpha: float = 0.1,
    gamma: float = 0.9,
    epsilon: float = 0.1,
    max_nb_cards: int = 3,
    max_card_value: int = 3,
    debug: bool = False,
):
    agent = QLearningAgent(
        alpha=alpha,
        gamma=gamma,
        epsilon=epsilon,
        max_cards=max_nb_cards,
        max_value=max_card_value,
    )
    prev_q_table = QTable.empty()
    # Example of training loop
    # for episode in range(episodes):
    episode = 0
    prev_variability = 50.0
    variability = 100.0
    epsilon_variability = 5.0
    # Track the number of times variability does not change significantly
    stable_count = 0
    stable_threshold = 5  # Number of consecutive checks to consider stabilized

    while stable_count < stable_threshold:
        episode += 1

        game_state = GameState.initialize_game(max_value=max_card_value)
        player_state: PlayerState = create_valide_player_state(
            n_cards=None, max_nb_cards=max_nb_cards, max_card_value=max_card_value
        )
        game_state.remove_cards(player_state.deck)
        done = False
        while not done:
            if debug:
                print()
                print(f"player_state: {player_state}")

            action: Action = agent.selection_action(player_state)
            next_player_state = player_state
            reward = 0.0
            if action == Action.STOP:
                is_bust: bool = not player_state.is_valid(max_nb_cards)
                reward: float = player_state.get_reward(action, is_bust=is_bust)
                done = True
            else:  # Action.TAKE
                next_player_state: PlayerState = one_step(
                    game_state, player_state, action
                )
                bust: bool = not next_player_state.is_valid(max_nb_cards)
                if bust:  # Failed
                    reward = player_state.get_reward(action, is_bust=True)
                    done = True
                elif len(player_state.deck) >= max_nb_cards:  # End of the game
                    reward = player_state.get_reward(action, is_bust=False)
                    done = True
            agent.update_q_value(player_state, action, reward, next_player_state, done)

            if not done:
                player_state = next_player_state

            if debug:
                print(f"action: {action.name}")
                print(f"next_player_state: {next_player_state}")
                print(f"reward: {reward}")

        if episode % 10_000 == 0:
            print(
                f"Episode {episode} - Variability : {variability}, previous variability: {prev_variability}"
            )
            prev_variability = variability
            variability: float = agent.q_table.variability(prev_q_table)
            prev_q_table = agent.q_table.__deepcopy__()
            if abs(variability - prev_variability) <= epsilon_variability:
                stable_count += 1
            else:
                stable_count = 0

    print(
        f"Episode {episode} - Variability : {variability}, previous variability: {prev_variability}"
    )
    return agent.q_table


# def q_table(n: int, nb_simulations: int) -> Dict[Tuple, Dict[Action, List[float]]]:
#     q_table: Dict[Tuple, Dict[Action, List[float]]] = {}
#     for i in range(n):
#         # player_state = create_valided_player_state()
#         player_state = PlayerState(deck=[i])
#         game_state = GameState.initialize_game()
#         game_state.remove_cards(player_state.deck)
#         values: Dict[Action, float] = compute_expected_rewards(
#             random_player,
#             game_state,
#             player_state,
#             nb_simulations=nb_simulations,
#             debug=False,
#         )
#         # Ensure the player_state is in the q_table
#         player_state_tuple = player_state.get_tuple()
#         if player_state_tuple not in q_table:
#             q_table[player_state_tuple] = {}
#         for action, value in values.items():
#             if action not in q_table[player_state_tuple]:
#                 q_table[player_state_tuple][action] = []
#             q_table[player_state_tuple][action].append(value)
#     return q_table
#     return q_table
