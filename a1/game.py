"""
Code for Game class and its subclass.
"""
from typing import Any
from state import State, SubtractState, ChopState


class Game:
    """
    A class which represents a general game.

    current_state - the current state of game
    is_p1_turn - p1 turn
    """
    current_state: State
    is_p1_turn: bool

    def __init__(self, is_p1_turn: bool)-> None:
        """
        Initialize a new game.
        """
        self.is_p1_turn = is_p1_turn

    def __eq__(self, other: Any) -> bool:
        """
        Return whether self is equivalent to other.
        """
        raise NotImplementedError("Override it!")

    def __str__(self) -> str:
        """
        Return an informative string about self.
        """
        raise NotImplementedError("Override it!")

    def get_instructions(self)-> str:
        """
        Return a string which contains the instruction of how to play the game.
        """
        raise NotImplementedError("Override it!")

    def str_to_move(self, move: str)-> str:
        """
        Return a string which reprents the move.

        >>> chop = Chopsticks(True)
        >>> chop.str_to_move("ll")
        'll'
        """
        return move

    def is_over(self, current_state: "State") -> bool:
        """
        Return whether the game of current_state is over.

        >>> chopstate = ChopState(True, [1,1], [1,3])
        >>> chopgame = Chopsticks(True)
        >>> chopgame.is_over(chopstate)
        False
        >>> chopstate = ChopState(True, [0,0], [1,3])
        >>> chopgame = Chopsticks(True)
        >>> chopgame.is_over(chopstate)
        True
        """
        return len(current_state.get_possible_moves()) == 0

    def is_winner(self, player: str)-> bool:
        """
        Return whether the player is winner.

        >>> chopgame = Chopsticks(True)
        >>> chopgame.current_state = ChopState(True, [1,1], [1,3])
        >>> chopgame.is_over(chopgame.current_state)
        False
        >>> chopgame.is_winner("p1")
        False
        >>> chopgame = Chopsticks(False)
        >>> chopstate = ChopState(False, [0,0], [1,3])
        >>> chopgame.current_state = chopstate
        >>> chopgame.is_over(chopgame.current_state)
        True
        >>> chopstate.get_current_player_name() == 'p2'
        True
        >>> chopgame.is_winner('p2')
        False

        """
        return (self.is_over(self.current_state)
                and self.current_state.get_current_player_name() != player)


class SubtractSquare(Game):
    """
    A class which represents a SubstractSquare game.

    current_state - a SubstractSquare state
    is_p1_turn - the turn of p1
    current_val - the current value
    """
    current_state: SubtractState
    is_p1_turn: bool
    current_val: int

    def __init__(self, is_p1_turn: bool) -> None:
        """
        Initialzie a new SubtratctSquare game.

        extends Game.__init__(is_p1_turn)
        """
        Game.__init__(self, is_p1_turn)
        current_val = int(input("Enter a number: "))
        self.current_val = current_val
        self.current_state = SubtractState(is_p1_turn, current_val)

    def __str__(self) -> str:
        """
        Return an informative string about self which contains the current\
        palyer and the current value.

        over-rides Game.__str__()
        """
        return SubtractState(self.is_p1_turn, self.current_val).__str__()

    def __eq__(self, other: Any) -> bool:
        """
        Return whether self is equivalent to other.

        over-rides Game.__eq__(other)
        """
        return (type(self) == type(other)
                and self.is_p1_turn == other.is_p1_turn
                and self.current_val == other.current_val
                and self.current_state == other.current_state)

    def get_instructions(self) -> str:
        """
        Return a string which contains the instruction of how to play the\
         game SubstractSquare.

        over-rides Game.get_instrcutions()
        """
        return "1). Each of two players begins with one finger pointed" +\
               "up on each of their hands. 2). Player A touches one hand" +\
               "to one of Player B's hands, increasing the number of fingers" +\
               "pointing up on Player B's hand by the number on Player A's " +\
               "hand. The number pointing up on Player A's hand remains " +\
               "the same. 3). If Player B now has five fingers up, that " +\
               "hand becomes dead or unplayable. If the number of fingers" +\
               "should exceed five, subtract five from the sum. 4). Now" +\
               "Player B touches one hand to one of Player A's hands, and" +\
               "the distribution of fingers proceeds as above, including " + \
               "the possibility of a dead hand.5. Play repeats steps 2-4 " + \
               "until some player has two dead hands, thus losing."


class Chopsticks(Game):
    """
    A class which represents a Chopsticks game.

    current_state - a Chopsticks State
    is_p1_turn - the turn of p1
    p1_state - the state of player 1
    p2_state - the state of player 2
    """
    current_state: ChopState
    is_p1_turn: bool
    p1_state: list
    p2_state: list

    def __init__(self, is_p1_turn: bool) -> None:
        """
        Initialize a new Chopsticks game.

        extends Game.__init__(is_p1_turn)
        """
        Game.__init__(self, is_p1_turn)
        self.p1_state = [1, 1]
        self.p2_state = [1, 1]
        self.current_state = ChopState(self.is_p1_turn,
                                       self.p1_state,
                                       self.p2_state)

    def __eq__(self, other: Any) -> bool:
        """
        Return whether self is equivalent to other.

        over-rides Game.__eq__(other)

        >>> chop1 = Chopsticks(True)
        >>> chop2 = Chopsticks(True)
        >>> chop1 == chop2
        True
        >>> chop2.p1_state = [2,3]
        >>> chop1 == chop2
        False
        """
        return (type(self) == type(other)
                and self.current_state == other.current_state
                and self.is_p1_turn == other.is_p1_turn
                and self.p1_state == other.p1_state
                and self.p2_state == other.p2_state)

    def __str__(self) -> str:
        """
        Return an informative string about self which includes the name \
        of current player and the current states of player 1 and player 2.

        over-rides Game.__str__()

        >>> chop = Chopsticks(True)
        >>> chop.__str__()
        'Player 1: 1-1; Player 2: 1-1, the current player is p1.'
        >>> chop = Chopsticks(True)
        >>> chop.p1_state = [3,4]
        >>> chop.__str__()
        'Player 1: 3-4; Player 2: 1-1, the current player is p1.'
        """
        return ChopState(self.is_p1_turn, self.p1_state,
                         self.p2_state).__str__()

    def get_instructions(self) -> str:
        """
        Return a string which contains the instruction of\
         how to play the ChopSticks game.

        over-rides Game.get_instructions()

        >>> chop = Chopsticks(True)
        >>> instruction = chop.get_instructions()
        >>> s = "1). A non-negative whole number is chosen as the starting" +\
               "value by some neutral entity. In our case, a player will " +\
               "choose it. 2). The player whose turn it is chooses some" +\
               "square of a positive whole number (such as 1, 4, 9, 16, " +\
               ". . . ) to subtract from the value, provided the chosen" +\
               " square is not larger. After subtracting, we have a new" +\
               "value and the next player chooses a square to subtract" +\
               "from it. 3). Play continues to alternate between the two" +\
               "players until no moves are possible. Whoever is about to" +\
               "play at that point loses!"
        >>> s == instruction
        True
        """
        return "1). A non-negative whole number is chosen as the starting" +\
               "value by some neutral entity. In our case, a player will " +\
               "choose it. 2). The player whose turn it is chooses some" +\
               "square of a positive whole number (such as 1, 4, 9, 16, " +\
               ". . . ) to subtract from the value, provided the chosen" +\
               " square is not larger. After subtracting, we have a new" +\
               "value and the next player chooses a square to subtract" +\
               "from it. 3). Play continues to alternate between the two" +\
               "players until no moves are possible. Whoever is about to" +\
               "play at that point loses!"


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config="a1_pyta.txt")
