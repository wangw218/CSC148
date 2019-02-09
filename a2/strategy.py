"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
import copy
from typing import Any, List, Dict
from game import Game



def interactive_strategy(game: Game) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def rough_outcome_strategy(game: Any) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2  # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move


def score(game: Game) -> int:
    """
    Return the best score of the current player of the state.
    """
    player = game.current_state.get_current_player_name()
    if player == 'p1':
        other = 'p2'
    else:
        other = 'p1'
    if game.is_over(game.current_state):
        if game.is_winner(player):
            return 1
        if game.is_winner(other):
            return -1
        return 0
    lst = []
    for move in game.current_state.get_possible_moves():
        new_game = copy.deepcopy(game)
        new_game.current_state = game.current_state.make_move(move)
        lst.append(new_game)
    return max([-1 * score(new_game) for new_game in lst])


def recursive_minimax(game: Game) -> Any:
    """
    Return a best move of the game for the current player to win through
    recursive minimax strategy.
    """
    lst = []
    for move in game.current_state.get_possible_moves():
        new_game = copy.deepcopy(game)
        new_game.current_state = game.current_state.make_move(move)
        s = -1 * score(new_game)
        lst.append([move, s])
    for e in lst:
        if e[1] == 1:
            return e[0]
    return lst[0][0]


# TODO: Implement an iterative version of the minimax strategy.
class Tree:
    """
    A class which used to record the current game's score and its children.

    game -  the game
    score - the current game's score
    childeren - the childeren of the current game
    """
    game: Game
    score: int
    children: List['Tree']

    def __init__(self, game: Game, children: List['Tree'] = None) -> None:
        """
        Create Tree self as a contioner containing the state and the state's
        score and the state's childeren.
        """
        self.game = game
        self.score = 0
        self.children = children.copy() if children else []


def tree_score(game: Game, snd) -> int:
    """
    Return the best score of the current player of the current game.
    """
    tree = Tree(game)
    stack = [tree]
    while stack:
        tree = stack.pop()
        if tree.children == [] and \
                (not tree.game.is_over(tree.game.current_state)):
            stack.append(tree)
            for move in tree.game.current_state.get_possible_moves():
                new_game = copy.deepcopy(game)
                new_game.current_state = tree.game.current_state.make_move(move)
                tree.children.append(Tree(new_game))
                stack.append(Tree(new_game))
        elif tree.children == [] and tree.game.is_over(tree.game.current_state):
            player = tree.game.current_state.get_current_player_name()
            if player == 'p1':
                other = 'p2'
            else:
                other = 'p1'
            if game.is_winner(player):
                tree.score = 1
            if game.is_winner(other):
                tree.score = -1
            else:
                tree.score = 0
        else:
            tree.score = max([-1 * child.score for child in tree.children])
    return tree.score


def iterative_minimax(game: Game) -> Any:
    """
    Return a best move of the game for the current player to win
    through iterative minimax strategy.
    """
    lst = []
    for move in game.current_state.get_possible_moves():
        new_game = copy.deepcopy(game)
        new_game.current_state = game.current_state.make_move(move)
        s = -1 * tree_score(new_game)
        lst.append([move, s])
    for e in lst:
        if e[1] == 1:
            return e[0]
    return lst[0][0]


if __name__ == "__main__":
    from python_ta import check_all

    check_all(config="a2_pyta.txt")
