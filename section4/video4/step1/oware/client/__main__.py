import socket
import pickle
import rx, rx.operators as ops
from pathlib import Path
from kivy.config import Config
from kivy.resources import resource_add_path
from kivy.properties import NumericProperty, ObjectProperty
from kivy.clock import Clock, mainthread
from kivy.app import App
from . import widgets
from ..model.board import Board
from ..util import ByteFIFO

resource_add_path(str(Path(widgets.__file__).resolve().parent / "data"))
Config.set("graphics", "width", 1365)
Config.set("graphics", "height", 768)


def try_recv(sock):
    try:
        return sock.recv(512)
    except BlockingIOError as x:
        # Resource Temporarily Unavailable error, which we can safely
        # ignore. It just means there's currently no data to receive.
        return b''

class OwareClientApp(App):
    board = ObjectProperty(None)
    player = NumericProperty(0)

    def on_start(self):
        self.sock = sock = socket.socket()

        try:
            sock.connect(('127.0.0.1', 60000))
        except ConnectionRefusedError:
            print("The Oware server is not running")
            raise SystemExit

        sock.setblocking(False)

        sched = rx.concurrency.ThreadPoolScheduler()

        rx.interval(0.5, sched).pipe(
            ops.map(lambda _: try_recv(sock)),
            ops.map(ByteFIFO().add),
            ops.flat_map(self.decode)
        ).subscribe_(on_next = self.receive, on_error = print)

    def decode(self, buffer):
        found = []
        offset = 0

        received = buffer.as_file()

        while True:
            try:
                found.append(pickle.load(received))
                offset = received.tell()
            except EOFError:
                break

        buffer.remove(offset)

        return rx.from_iterable(found)

    @mainthread
    def receive(self, data):
        print('received', data)
        self.player = data.get('player', self.player)
        self.board = data.get('board', self.board)

    def on_board(self, instance, value):
        for house_widget, house_value in zip(
            self.root.houses, value.houses_for_player(self.player)
        ):
            house_widget.seeds = house_value

    def sow_from(self, house_index):
        if house_index > 5:
            return

        self.sock.send(pickle.dumps((self.player, house_index)))

if __name__ == "__main__":
    OwareClientApp().run()
