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
import os

if __name__ == "__main__":
    # qtable: QTable = q_learning_strategy(
    #     10_000_000,
    #     max_nb_cards=7,
    #     max_card_value=13,
    #     debug=False,
    #     epsilon_percentage=0.03,
    # )
    qtable: QTable = QTable.empty()
    qtable.load_q_table("q_table.pkl")

    print(qtable)
    output_path = "q_table.txt"
    # Ensure the file exists (will create if not)
    if not os.path.exists(output_path):
        open(output_path, "w").close()

    with open(output_path, "w") as f:
        for state, actions in qtable.values.items():
            f.write(f"{state}: {actions}\n")
