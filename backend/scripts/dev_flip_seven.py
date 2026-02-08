from typing import Dict, List

from chatbot.flip_seven.game import (
    compute_expected_rewards,
    create_valided_player_state,
    game_loop,
    one_step,
)
from chatbot.flip_seven.models import Action, GameState, PlayerState
from chatbot.flip_seven.player import draw_player, random_player
from chatbot.flip_seven.strategy import q_table

if __name__ == "__main__":
    q_table_values = q_table(12, nb_simulations=50000)
    print(q_table_values)
