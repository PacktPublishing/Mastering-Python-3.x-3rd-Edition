from typing import List, Tuple
import asyncio
import pickle
from ..model.board import Board
from ..util import ByteFIFO


class Player:
    def __init__(self: Player, player_id: int, writer: asyncio.StreamWriter):
        if player_id > 1:
            raise RuntimeError("Only two players are supported at once")

        self.player_id = player_id
        self.writer = writer
        self.fifo: ByteFIFO = ByteFIFO()

    async def send_board_state(self: Player, board: Board) -> None:
        self.writer.write(pickle.dumps(dict(player=self.player_id, board=board)))
        await self.writer.drain()

    async def read_move(self: Player) -> int:
        while True:
            f = self.fifo.as_file()

            try:
                # In the real world, pickles *should not* be sent over
                # the network, or more to the point, they should not
                # be received and decoded from the network. This poor
                # choice was included in the code to give us a chance
                # to talk about why it's a bad idea.
                move: Tuple[int, int] = pickle.load(f)
            except EOFError:
                await self.fifo.more_data()
            else:
                self.fifo.remove(f.tell())

                if move[0] != self.player_id:
                    raise ValueError("Incorrect player id received")

                return move[1]


class Game:
    def __init__(self: Game):
        self.players: List[Player] = []

    async def send_board_state(self: Game, board: Board) -> None:
        for player in self.players:
            await player.send_board_state(board)

    async def turn(self: Game, board: Board, player_id: int) -> Board:
        house = await self.players[player_id].read_move()
        board = board.sow(player_id, house)

        while board.valid_moves:
            await self.players[player_id].send_board_state(board)
            house = await self.players[player_id].read_move()
            board = board.sow(player_id, house)

        return board

    async def turns(self: Game) -> None:
        board = Board()

        await self.send_board_state(board)

        while not board.winners:
            board = await self.turn(board, 0)
            await self.send_board_state(board)

            # !!! if board.winners: break

            board = await self.turn(board, 1)
            await self.send_board_state(board)

        await self.send_board_state(board)

    async def player(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        player = Player(len(self.players), writer)

        self.players.append(player)

        if player.player_id == 1:
            asyncio.create_task(self.turns())

        while True:
            player.fifo.add(await reader.read(4096))


async def main() -> None:
    game: Game = Game()

    service = await asyncio.start_server(game.player, host="127.0.0.1", port=60000)
    await service.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
