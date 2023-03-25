from socket import socket, AF_INET, SOCK_STREAM
from .match.matchmaking import MatchMaking
from .malloc.room import Room
from .player_info.player import Player
from .rule.tictactoe import TicTacToe
from typing import Any
from dataclasses import dataclass, field
import time


def get_time() -> str:
    return time.strftime("%Y.%m.%d - %H:%M:%S")


@dataclass(frozen=True, kw_only=True)
class Config:
    IP: str
    PORT: int
    backlog: int
    number_of_room: int
    created_at: str = field(default_factory=get_time)


class TicTacToeServer:
    def __init__(self) -> None:
        self.matchmaker: MatchMaking
        self.listener: socket
        self.rooms: dict[int, Room]
        self.ids: list[int]
        self.room_count: int = 0

    def setting(self, config: Config) -> None:
        self.listener = socket(AF_INET, SOCK_STREAM)
        self.listener.bind((config.IP, config.PORT))
        self.listener.listen(config.backlog)
        self.listener.setblocking(False)
        self.ids = [_id for _id in range(config.number_of_room)]
        self.rooms = {}
        self.matchmaker = MatchMaking(2)

    def update(self) -> None:
        client: socket
        address: Any
        try:
            client, address = self.listener.accept()
            self.matchmaker.push(Player(client, address))
            print("Accepted", len(self.matchmaker.player_list))
        except:
            ...
        players: list[Player] = self.matchmaker.match()
        if len(players) == 2:
            self.rooms[self.ids.pop()] = Room(rule=TicTacToe, players=players)
            self.room_count += 1
            print("Mached", self.room_count)
        call_back: list[int] = []
        for room_id, room in self.rooms.items():
            room.update()
            if room.end_check:
                room.close()
                call_back.append(room_id)
        for room_id in call_back:
            self.room_count -= 1
            print(self.rooms[room_id].info, self.room_count)
            self.rooms.pop(room_id)
            self.ids.append(room_id)
