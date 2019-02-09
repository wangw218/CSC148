"""
Code for two strategies: interactive_strategy and random_strategy.
"""
import random
from game import Game


def interactive_strategy(game: Game) -> str:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def random_strategy(game: Game) -> str:
    """
    Return a random move for game.
    """
    move = game.current_state.get_possible_moves()
    h = random.randrange(0, len(move))
    return move[h]


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config="a1_pyta.txt")
