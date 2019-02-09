"""
Code for State Class and its two subclass.
"""
from typing import Any, List


class State:
    """
    A class of the state of a game.

    is_p1_turn - the turn of p1
    """

    is_p1_turn: bool

    def __init__(self, is_p1_turn: bool) -> None:
        """
        Initialize a new state.
        """
        self.is_p1_turn = is_p1_turn

    def __str__(self) -> str:
        """
        Return an informative string about self.
        """
        raise NotImplementedError("Override it!")

    def __eq__(self, other: Any) -> bool:
        """
        Return whether self is equivalent to other.
        """
        raise NotImplementedError("Override it!")

    def get_current_player_name(self) -> str:
        """
        Return the name of current palyer.

        >>> State(True).get_current_player_name()
        'p1'
        >>> State(False).get_current_player_name()
        'p2'
        """
        if self.is_p1_turn is True:
            player = 'p1'
        else:
            player = 'p2'
        return player

    def get_possible_moves(self) -> List[str]:
        """
        Return a list of str which contains the possible moves.
        """
        raise NotImplementedError("Override it!")

    def is_valid_move(self, move_to_make: str) -> bool:
        """
        Return whether move_to_make is a a valid move.

        >>> square = SubtractState(True,8)
        >>> square.get_possible_moves()
        ['1', '4']
        >>> square.is_valid_move('1')
        True
        >>> square.is_valid_move('8')
        False
        >>> chop = ChopState(True, [1,0], [1,2])
        >>> chop.get_possible_moves()
        ['ll', 'lr']
        >>> chop.is_valid_move('ll')
        True
        >>> chop.is_valid_move('rl')
        False
        """
        return move_to_make in self.get_possible_moves()

    def make_move(self, move_to_make: str) -> "State":
        """
        Return the a new state after making a move move_to_make.
        """
        raise NotImplementedError("Override it!")


class SubtractState(State):
    """
    A class of the state of a SubtrractSquare game.

    is_p1_turn - the turn of p1
    current_val - the current value
    """

    is_p1_turn: bool
    current_val: int

    def __init__(self, is_p1_turn: bool, current_val: int) -> None:
        """
        Initialize a new state of SubtractSquare game.

        extends State.__init__(is_p1_turn)
        """
        State.__init__(self, is_p1_turn)
        self.current_val = current_val

    def __str__(self) -> str:
        """
        Return an informative string about self which contains \
        the current player and the current value.

        over-rides State.__str__()

        >>> SubtractState(True,8).__str__()
        'The current player is p1 and the current value is 8.'
        >>> SubtractState(False,12).__str__()
        'The current player is p2 and the current value is 12.'
        """
        return "The current player is {} and the current value is {}.".format(
            self.get_current_player_name(), self.current_val)

    def __eq__(self, other: Any) -> bool:
        """
        Return whether self is equivalent to other.

        >>> SubtractState(True,8) == SubtractState(False,12)
        False
        >>> SubtractState(True,8) == SubtractState(True,8)
        True
        """
        return (type(self) == type(other)
                and self.current_val == other.current_val
                and self.is_p1_turn == other.is_p1_turn)

    def get_possible_moves(self) -> List[str]:
        """
        Return a list of str which contains the possible moves.

        over-rides State.get_possible_moves()

        >>> square = SubtractState(True,8)
        >>> square.get_possible_moves()
        ['1', '4']
        >>> square.current_val = 20
        >>> square.get_possible_moves()
        ['1', '4', '9', '16']
        """
        return [str(i**2) for i in range(1, self.current_val + 1)
                if i**2 <= self.current_val]

    def make_move(self, move_to_make: str) -> "SubtractState":
        """
        Return the a new SubstractSquare state after making \
        a move move_to_make.

        over_rides State.make_move(move_to_make)

        >>> square = SubtractState(True,8)
        >>> square.get_possible_moves()
        ['1', '4']
        >>> state = square.make_move('1')
        >>> state == SubtractState(False, 7)
        True
        >>> square = SubtractState(True,8)
        >>> square.get_possible_moves()
        ['1', '4']
        >>> state = square.make_move('8')
        >>> state == SubtractState(True, 8)
        True
        """
        is_p1_turn = self.is_p1_turn
        current_val = self.current_val
        if self.is_valid_move(move_to_make):
            current_val = self.current_val - int(move_to_make)
            if self.is_p1_turn is True:
                is_p1_turn = False
            else:
                is_p1_turn = True
        return SubtractState(is_p1_turn, current_val)


class ChopState(State):
    """
    A class of the state of a Chopsticks game.

    is_p1_turn - the turn of p1
    p1_state - the state of player 1
    p2_state - the state of player 2
    p1_left - the number of left hand of player 1
    p1_right - the number of right hand of player 1
    p2_left - the number of left hand of player 2
    p2_right - the number of right hand of player 2

    """
    is_p1_turn: bool
    p1_state: list
    p2_state: list
    p1_left: int
    p1_right: int
    p2_left: int
    p2_right: int

    def __init__(self, is_p1_turn: bool, p1_state: list,
                 p2_state: list) -> None:
        """
        Initialize a new state of Chopsticks game.
        """
        State.__init__(self, is_p1_turn)
        self.p1_state, self.p2_state = p1_state, p2_state
        self.p1_left, self.p1_right = self.p1_state[0], self.p1_state[1]
        self.p2_left, self.p2_right = self.p2_state[0], self.p2_state[1]

    def __str__(self) -> str:
        """
        Return an informative string about self which includes \
        the name of current player and the current states\
        of player 1 and player 2.

        over-rides State.__str__()

        >>> state = ChopState(True, [1,1], [2,3])
        >>> state.__str__()
        'Player 1: 1-1; Player 2: 2-3, the current player is p1.'
        >>> state = ChopState(False, [1,1], [2,4])
        >>> state.__str__()
        'Player 1: 1-1; Player 2: 2-4, the current player is p2.'
        """
        return "Player 1: {}-{}; Player 2: {}-{}, the current player is {}."\
            .format(self.p1_left, self.p1_right, self.p2_left, self.p2_right,
                    self.get_current_player_name())

    def __eq__(self, other: Any) -> bool:
        """
        Return whether self is equivalent to other.

        over-rides State.__eq__()

        >>> ChopState(True, [1,1], [2,3]) == ChopState(True, [1,1], [2,3])
        True
        >>> ChopState(False, [1,1], [2,4]) == ChopState(True, [1,1], [2,3])
        False
        """
        return (type(self) == type(other)
                and self.p1_state == other.p1_state
                and self.p2_state == other.p2_state)

    def get_possible_moves(self) -> List[str]:
        """
        Return a list of str which contains the possible moves.

        over-rides State.get_possible_moves()
        >>> chop = ChopState(True, [1,0], [1,2])
        >>> chop.get_possible_moves()
        ['ll', 'lr']
        >>> chop = ChopState(True, [1,4], [1,2])
        >>> chop.get_possible_moves()
        ['ll', 'lr', 'rl', 'rr']

        """
        lst = []
        if self.get_current_player_name() == 'p1':
            if self.p1_left != 0:
                if self.p2_left != 0:
                    lst.append('ll')
                if self.p2_right != 0:
                    lst.append('lr')
            if self.p1_right != 0:
                if self.p2_left != 0:
                    lst.append("rl")
                if self.p2_right != 0:
                    lst.append("rr")
        if self.get_current_player_name() == 'p2':
            if self.p2_left != 0:
                if self.p1_left != 0:
                    lst.append("ll")
                if self.p1_right != 0:
                    lst.append("lr")
            if self.p2_right != 0:
                if self.p1_left != 0:
                    lst.append("rl")
                if self.p1_right != 0:
                    lst.append("rr")
        return lst

    def make_move(self, move_to_make: str) -> "ChopState":
        """
        Return the a new ChopSticks state after making a move move_to_make.

        over_rides State.make_move(move_to_make)

        >>> chop = ChopState(True, [1,0], [1,2])
        >>> chop.get_possible_moves()
        ['ll', 'lr']
        >>> state = chop.make_move('ll')
        >>> state == ChopState(False, [1,0], [2,2])
        True
        >>> state = chop.make_move('rl')
        >>> state == ChopState(True, [1,0], [1,2])
        True
        """
        p1_left, p1_right = self.p1_state[0], self.p1_state[1]
        p2_left, p2_right = self.p2_state[0], self.p2_state[1]
        is_p1_turn = self.is_p1_turn
        p1_state, p2_state = self.p1_state, self.p2_state
        if self.is_valid_move(move_to_make):
            if self.get_current_player_name() == 'p1':
                if move_to_make == 'll':
                    p2_left = (self.p1_left + self.p2_left) % 5
                if move_to_make == 'lr':
                    p2_right = (self.p2_right + self.p1_left) % 5
                if move_to_make == "rl":
                    p2_left = (self.p2_left + self.p1_right) % 5
                if move_to_make == "rr":
                    p2_right = (self.p2_right + self.p1_right) % 5
            if self.get_current_player_name() == 'p2':
                if move_to_make == "ll":
                    p1_left = (self.p1_left + self.p2_left) % 5
                if move_to_make == "lr":
                    p1_right = (self.p1_right + self.p2_left) % 5
                if move_to_make == "rl":
                    p1_left = (self.p1_left + self.p2_right) % 5
                if move_to_make == "rr":
                    p1_right = (self.p1_right + self.p2_right) % 5
            p1_state, p2_state = [p1_left, p1_right], [p2_left, p2_right]
            if self.is_p1_turn is True:
                is_p1_turn = False
            else:
                is_p1_turn = True
        return ChopState(is_p1_turn, p1_state, p2_state)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config="a1_pyta.txt")
