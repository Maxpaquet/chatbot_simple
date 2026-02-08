import random
from enum import IntEnum
from typing import List

from pydantic import BaseModel


class Action(IntEnum):
    STOP = 0
    TAKE = 1


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
    def initialize_game(cls) -> "GameState":
        deck = [0, 1] + [i for i in range(2, 13) for _ in range(i)]
        # random.shuffle(deck)
        return cls(deck=deck)

    def draw_card(self) -> int:
        """Simulates drawing a card from a standard deck, returning a value between 1 and 10."""
        card: int = random.choice(self.deck)
        self.remove_cards(card)
        return card


class PlayerState(BaseModel):
    deck: List[int]

    def get_tuple(self):
        return tuple(sorted(self.deck))

    def score(self) -> int:
        return sum(self.deck)

    def get_reward(self) -> float:
        """Return -1 if there are duplicate cards in the player's deck, otherwise return the player's score."""
        if len(self.deck) == 0:
            return 0
        if len(set(self.deck)) != len(self.deck):
            return -1
        return self.score()
