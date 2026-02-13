import random
from itertools import permutations
from typing import Callable, List

from chatbot.flip_seven.models import Action, GameState, PlayerState


def create_valide_player_state(
    n_cards: int | None, max_nb_cards: int = 7, max_card_value: int = 13
) -> PlayerState:
    # Create a new GameState with a shuffled deck and an empty PlayerState
    all_cards = list(GameState.initialize_game(max_value=max_card_value).deck)
    random.shuffle(all_cards)

    player_state = PlayerState(deck=[])
    done = True
    while done:
        if n_cards is not None:
            n_cards = min(n_cards, max_nb_cards)
            # Draw n_cards randomly, ensuring all cards are unique
            initial_cards = random.sample(all_cards, n_cards)
        else:
            random_max_cards = random.randint(1, min(max_nb_cards, len(all_cards)))
            initial_cards = random.sample(all_cards, random_max_cards)
        player_state = PlayerState(deck=initial_cards)
        if player_state.is_valid(max_nb_cards):
            done = False
    return player_state


def create_all_valid_player_states(max_cards: int = 7) -> List[List[PlayerState]]:
    all_cards = list(GameState.initialize_game().deck)
    results = []
    for n in range(1, max_cards + 1):
        states_n = []
        for player_deck in permutations(all_cards, n):
            player_state = PlayerState(deck=list(player_deck))
            states_n.append(player_state)
        results.append(states_n)
    return results


def one_step(
    game_state: GameState, state_in: PlayerState, action: Action
) -> PlayerState:
    """Simulates one game of Flip Seven, where the player has choosen to take a card or stop."""
    if action == Action.TAKE:
        card = game_state.draw_card()
        return PlayerState(deck=state_in.deck + [card])
    else:
        return state_in


def game_loop(
    player: Callable[[PlayerState], Action],
    game_state: GameState,
    player_state: PlayerState,
    debug: bool = False,
) -> float:
    continue_flag = True
    total_score: float = 0.0
    # Simulate a few steps of the game
    while continue_flag:
        action: Action = player(player_state)
        if action == Action.STOP:
            break
        else:
            player_state = one_step(game_state, player_state, action)
            reward = player_state.get_reward()
            if reward == -1:
                if debug:
                    print(
                        f"[game_loop] STOP - Duplicate cards: {player_state.get_tuple()}"
                    )
                return -1
            else:
                total_score = reward
    return total_score


# def compute_expected_rewards(
#     player: Callable[[PlayerState], Action],
#     game_state: GameState,
#     player_state: PlayerState,
#     nb_simulations: int = 1000,
#     debug: bool = False,
# ):
#     res: Dict[Action, float] = {}
#     for action in Action:
#         expected_reward = 0.0
#         for _ in range(nb_simulations):
#             game_state_ = game_state.__deepcopy__()
#             # Simulate one step with the given action
#             state_after_one_step: PlayerState = one_step(
#                 game_state_, player_state, action
#             )
#             reward_after_one_step = state_after_one_step.get_reward()
#             if reward_after_one_step == -1:
#                 if debug:
#                     print(
#                         f"Simulation reward: {reward_after_one_step} (STOP - Duplicate cards)"
#                     )
#                 # Reward of 0 for this simulation, since the player would have lost immediately
#                 reward_score_lap = 0.0
#             else:
#                 reward_score_lap: float = game_loop(
#                     player, game_state_, state_after_one_step, debug=debug
#                 )
#                 if debug:
#                     print(f"Simulation reward: {reward_score_lap}")
#             expected_reward += reward_score_lap
#         expected_reward /= nb_simulations
#         if debug:
#             print(
#                 f"Expected reward after {nb_simulations} simulations: {expected_reward}"
#             )
#         res[action] = expected_reward
#     return res
