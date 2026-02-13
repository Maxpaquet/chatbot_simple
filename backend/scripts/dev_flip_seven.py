from typing import Dict, List

from chatbot.flip_seven.game import (
    create_all_valid_player_states,
    create_valide_player_state,
    game_loop,
    one_step,
)
from chatbot.flip_seven.models import Action, GameState, PlayerState, QTable
from chatbot.flip_seven.player import draw_player, random_player
from chatbot.flip_seven.strategy import QLearningAgent, q_learning_strategy

if __name__ == "__main__":
    print(q_learning_strategy(1_000_000, max_nb_cards=3, max_card_value=8, debug=False))
