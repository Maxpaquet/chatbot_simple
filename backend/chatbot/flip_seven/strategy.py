from typing import Dict, List, Tuple

from chatbot.flip_seven.game import (
    compute_expected_rewards,
    create_valided_player_state,
    game_loop,
    one_step,
)
from chatbot.flip_seven.models import Action, GameState, PlayerState
from chatbot.flip_seven.player import draw_player, random_player


def q_table(n: int, nb_simulations: int) -> Dict[Tuple, Dict[Action, List[float]]]:
    q_table: Dict[Tuple, Dict[Action, List[float]]] = {}
    for i in range(n):
        # player_state = create_valided_player_state()
        player_state = PlayerState(deck=[i])
        game_state = GameState.initialize_game()
        game_state.remove_cards(player_state.deck)
        values: Dict[Action, float] = compute_expected_rewards(
            random_player,
            game_state,
            player_state,
            nb_simulations=nb_simulations,
            debug=False,
        )
        # Ensure the player_state is in the q_table
        player_state_tuple = player_state.get_tuple()
        if player_state_tuple not in q_table:
            q_table[player_state_tuple] = {}
        for action, value in values.items():
            if action not in q_table[player_state_tuple]:
                q_table[player_state_tuple][action] = []
            q_table[player_state_tuple][action].append(value)
    return q_table
