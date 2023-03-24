from typing import TYPE_CHECKING, Any
from json import loads

if TYPE_CHECKING:
    from player_info.player import Player


class TicTacToe:
    def __init__(self, players: list["Player"]) -> None:
        self.end: bool = False
        self.players: list["Player"] = players
        for player in self.players:
            player.sock.setblocking(False)
        self.color: int = 0

    def update(self) -> None:
        if self.end:
            return
        check: bool = False
        for p in self.players:
            check = p.state
        self.end = check
        try:
            msg: bytes = self.players[self.color % 2].sock.recv(2048)
            if len(msg) == 0:
                return
            data: Any = loads(msg)
            self.end = data["state"]
            self.color += 1
            self.players[self.color % 2].sock.send(msg)
        except:
            ...

    def close(self) -> None:
        for p in self.players:
            p.sock.close()
