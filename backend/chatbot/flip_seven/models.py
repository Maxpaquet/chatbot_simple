import random
from copy import deepcopy
from enum import IntEnum
from typing import Dict, List, Tuple

from pydantic import BaseModel


class Action(IntEnum):
    STOP = 0
    TAKE = 1

    def get_random_action(self) -> "Action":
        return random.choice(list(Action))


class GameState(BaseModel):
    deck: List[int]

    def get_tuple(self):
        return tuple(sorted(self.deck))

    def remove_cards(self, card_or_cards: int | List[int]) -> None:
        if isinstance(card_or_cards, List):
            for card in card_or_cards:
                self.deck.remove(card)
        else:
            self.deck.remove(card_or_cards)

    @classmethod
    def initialize_game(cls, max_value: int = 13) -> "GameState":
        deck = [0, 1] + [i for i in range(2, max_value + 1) for _ in range(i)]
        # random.shuffle(deck)
        return cls(deck=deck)

    def draw_card(self) -> int:
        """Simulates drawing a card from a standard deck, returning a value between 1 and 10."""
        card: int = random.choice(self.deck)
        self.remove_cards(card)
        return card


class PlayerState(BaseModel):
    deck: List[int]

    def is_valid(self, max_nb_cards: int) -> bool:
        """Checks if the player's state is valid (i.e., no duplicate cards)."""
        if len(self.deck) <= max_nb_cards and len(set(self.deck)) == len(self.deck):
            return True
        return False

    def get_tuple(self) -> Tuple[int, ...]:
        return tuple(sorted(self.deck))

    def score(self) -> int:
        return sum(self.deck)

    def get_reward(self, action: Action, is_bust: bool) -> float:
        """Return -1 if there are duplicate cards in the player's deck, otherwise return the player's score."""
        if is_bust:
            return -5.0  # Punition pour avoir perdu
        if action == Action.STOP:
            return float(self.score())  # Récompense réelle
        return 0.0


class QTable:
    # values: Dict[Tuple, Dict[Action, float]] = {}

    def __init__(
        self,
        values: Dict[Tuple[int, ...], Dict[Action, float]],
        possible_actions: List[Action],
    ):
        # Le dictionnaire principal : {état_tuple: {action: valeur_q}}
        self.values: Dict[Tuple[int, ...], Dict[Action, float]] = values
        self.possible_actions = possible_actions

    def __deepcopy__(self):
        memo = None
        copied_values = deepcopy(self.values, memo)
        copied_actions = deepcopy(self.possible_actions, memo)
        return QTable(copied_values, copied_actions)

    @classmethod
    def empty(cls) -> "QTable":
        """Retourne un dictionnaire de valeurs et une liste d'actions vides."""
        return cls(values={}, possible_actions=[])

    def __str__(self) -> str:
        res: List = []
        for state, actions in self.values.items():
            actions_str = ", ".join(
                f"{action.name}, {value:.2f}" for action, value in actions.items()
            )
            res.append(f"State {state} - {actions_str}")
        return "\n".join(res)

    def get_q_value(self, state: PlayerState, action: Action) -> float:
        state_tuple: Tuple[int, ...] = state.get_tuple()
        if state_tuple not in self.values:
            return 0.0
        return self.values[state_tuple][action]

    def set_q_value(self, state: PlayerState, action: Action, value: float) -> None:
        state_tuple: Tuple[int, ...] = state.get_tuple()
        if state_tuple in self.values:
            self.values[state_tuple][action] = value

    def get_max_q(self, state: Tuple[int, ...]) -> float:
        """Récupère la valeur Q maximale possible pour un état donné."""
        if state not in self.values or not self.values[state]:
            return 0.0
        return max(self.values[state].values())

    def get_best_action(self, state: Tuple[int, ...]) -> Action:
        """Retourne l'action avec la valeur Q la plus élevée pour un état."""
        if state not in self.values or not self.values[state]:
            Action.TAKE
        q_values = self.values[state]
        return max(q_values, key=q_values.__getitem__)

    def variability(self, other: "QTable") -> float:
        """
        Compute the sum of absolute differences between two Q-tables.
        For states present in both, sum the abs diff for all actions.
        For states present in only one, sum the abs values for all actions in that state.
        """
        total_diff = 0.0
        count = 0
        all_states = set(self.values.keys()).union(other.values.keys())
        for state in all_states:
            actions_self = self.values.get(state, {})
            actions_other = other.values.get(state, {})
            all_actions = set(actions_self.keys()).union(actions_other.keys())
            for action in all_actions:
                val_self = actions_self.get(action)
                val_other = actions_other.get(action)
                if val_self is not None and val_other is not None:
                    total_diff += abs(val_self - val_other)
                    count += 1
                elif val_self is not None:
                    total_diff += abs(val_self)
                    count += 1
                elif val_other is not None:
                    total_diff += abs(val_other)
                    count += 1
        return total_diff
