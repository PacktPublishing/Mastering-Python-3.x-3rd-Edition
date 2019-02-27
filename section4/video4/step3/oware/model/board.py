from typing import Iterable, Generator, List, Optional

OWNED = [(0, 1, 2, 3, 4, 5), (6, 7, 8, 9, 10, 11)]


def _counterclockwise(after: int, count: int) -> Iterable[int]:
    """Counts off `count` houses, in a counter-clockwise cycle of twelve.

    The first value returned is the house one step counter-clockwise
    from the `after` house.

    If the loop makes it all the way back to `after`, it is skipped.

    """

    into: int = after

    for i in range(count):
        into = (into + 1) % 12
        if into == after:
            into = (into + 1) % 12
        yield into


class Board:
    """Represents an Oware game state

    https://en.wikipedia.org/wiki/Oware

    """

    def __init__(self: Board, other: Optional[Board] = None):
        """Sets up the starting state of the game

        Initially, each of the twelve houses has four seeds in it,
        neither player has any captured seeds, and neither player has
        won.

        Alternately, the state can be a copy of the board state in
        `other`.

        """

        if other is None:
            self.houses: List[int] = [4] * 12
            self.captured: List[int] = [0, 0]
            self.winners: List[int] = []
            self.valid_moves: List[int] = []
        else:
            self.houses = list(other.houses)
            self.captured = list(other.captured)
            self.winners = list(other.winners)
            self.valid_moves = list(other.valid_moves)

    def houses_for_player(self: Board, player: int) -> Iterable[int]:
        if player == 0:
            yield from self.houses
        elif player == 1:
            yield from self.houses[6:]
            yield from self.houses[:6]
        else:
            raise ValueError(f"Invalid player number: {player}")

    def player_has_seeds(self: Board, player: int) -> bool:
        """Does the specified player have any seeds in their houses?"""
        return any(self.houses[x] for x in OWNED[player])

    def after_move(self: Board, player: int, player_house: int) -> Board:
        """Projects the game state into the future.

        The result is the next state, given a `player` choosing to sow
        house `player_house` on their side of the board.

        """

        next_state: Board = Board(self)

        starting_house: int = (player * 6) + player_house

        seeds: int = next_state.houses[starting_house]

        next_state.houses[starting_house] = 0

        house_stack: List[int] = []

        for house in _counterclockwise(starting_house, seeds):
            next_state.houses[house] += 1
            house_stack.append(house)

        if not house_stack:
            return next_state

        houses_before_capture: List[int] = list(next_state.houses)
        captured_before_capture: List[int] = list(next_state.captured)

        for house in reversed(house_stack):
            if house not in OWNED[not player]:
                break

            if next_state.houses[house] not in (2, 3):
                break

            next_state.captured[player] += next_state.houses[house]
            next_state.houses[house] = 0

        if not next_state.player_has_seeds(not player):
            next_state.houses = houses_before_capture
            next_state.captured = captured_before_capture

        if next_state.captured[player] >= 25:
            next_state.winners = [player]

        return next_state

    def sow(self: Board, player: int, player_house: int) -> Board:
        """Perform one Oware game move

        1) Pick a house owned by the current player. If the opponent
           has no seeds, the house chosen must be one that will result
           in the opponent having seeds after the move. If no such
           move is possible, all seeds within the current player's
           houses are claimed and the game is over. Whichever player
           has more seeds is the winner. If they both have 24 seeds
           the game is a tie.

        2) Remove the seeds from that house.

        3) Distribute the seeds one by one counter-clockwise,
           skipping the house that the seeds were removed from

        4) If the last seed distributed brought an opponent house to 2
           or 3 seeds, capture those seeds.

        5) Continue examing houses in reverse order of seed placement,
           and capturing the seeds, until reaching a house that does
           not contain 2 or 3 seeds, or is not owned by the opponent.

        6) If steps 4 and 5 would capture all of the opponents seeds,
           no captures occur.

        7) If the current player has 25 or more seeds, the game is
           over and the current player is the winner.

        """

        self.valid_moves: List[int] = []

        if not self.player_has_seeds(not player):
            possibilities: List[Board] = [self.after_move(player, x) for x in range(6)]
            validity: List[bool] = [x.player_has_seeds(not player) for x in possibilities]

            if not any(validity):
                for i in OWNED[player]:
                    self.captured[player] += self.houses[i]
                    self.houses[i] = 0

                if self.captured[player] >= 25:
                    self.winners = [player]
                elif self.captured[player] == 24:
                    self.winners = [player, not player]
                else:
                    self.winners = [not player]

                return self

            elif not validity[player_house]:
                self.valid_moves = [i for i, b in enumerate(validity) if b]
                return self

            else:
                return possibilities[player_house]

        return self.after_move(player, player_house)
