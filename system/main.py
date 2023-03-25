from socket import socket, AF_INET, SOCK_STREAM
from .match.matchmaking import MatchMaking
from .malloc.room import Room
from .player_info.player import Player
from .rule.tictactoe import TicTacToe
from typing import Any
import os


class TicTacToeServer:
    def __init__(self) -> None:
        self.matchmaker: MatchMaking
        self.listener: socket
        self.rooms: dict[int, Room]
        self.ids: list[int]
        self.room_count: int = 0

    def setting(self) -> None:
        ip: str = str(os.getenv("IP"))
        port: str = str(os.getenv("PORT"))
        if ip == "None" or port == "None":
            return
        self.listener = socket(AF_INET, SOCK_STREAM)
        self.listener.bind((ip, int(port)))
        self.listener.listen(20)
        self.listener.setblocking(False)
        self.ids = [_id for _id in range(10000)]
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
