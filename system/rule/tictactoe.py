from typing import TYPE_CHECKING, Any
from queue import Queue
from json import dumps

if TYPE_CHECKING:
    from player_info.player import Player


class TicTacToe:
    def __init__(self, players: list["Player"]) -> None:
        self.end: bool = False
        self.players: list["Player"] = players
        for player in self.players:
            player.sock.setblocking(False)
        self.color: int = 0
        self.players[0].sock.send('{"state": 0}'.encode())
        self.players[1].sock.send('{"state": 1}'.encode())

    def update(self) -> None:
        if self.end:
            return
        for p in self.players:
            self.end = not p.state
            if self.end:
                return
        msg_q: Queue[Any] = Queue()
        self.players[0].load(msg_q)
        while not msg_q.empty():
            self.players[1].sock.send(dumps(msg_q.get()).encode())
        self.players[1].load(msg_q)
        while not msg_q.empty():
            self.players[0].sock.send(dumps(msg_q.get()).encode())

    def close(self) -> None:
        for p in self.players:
            p.sock.close()
        print("Game Closed")
