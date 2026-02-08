import random

from chatbot.flip_seven.models import Action, PlayerState


def random_player(state: PlayerState) -> Action:
    """A simple player that randomly chooses to take a card or stop."""
    return random.choice(list(Action))


def draw_player(state: PlayerState) -> Action:
    return Action.TAKE


def stop_player(state: PlayerState) -> Action:
    return Action.STOP
