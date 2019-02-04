"""Minimal Oware server

This server doesn't actually implement the Oware game. It simply
allows a single client to connect, and speaks the game protocol well
enough to allow that client to run.

"""

import pickle
import socket
from ..model.board import Board
from ..util import ByteFIFO

def main():
    board = Board()

    ear = socket.socket()
    ear.bind(('127.0.0.1', 60000))
    ear.listen(5)

    sock, addr = ear.accept()

    sock.send(pickle.dumps(dict(player = 0, board = board)))

    fifo = ByteFIFO()

    try:
        while True:
            fifo.add(sock.recv(4046))

            f = fifo.as_file()

            try:
                move = pickle.load(f)
            except EOFError:
                pass
            else:
                fifo.remove(f.tell())
                print(f"Player {move[0] + 1} from {move[1]}")
                sock.send(pickle.dumps(dict(board = board)))
    finally:
        sock.close()

if __name__ == '__main__':
    main()
