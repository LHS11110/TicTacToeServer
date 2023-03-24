from socket import socket
from queue import Queue
from json import loads
from typing import Any
import traceback


class Player:
    def __init__(self, sock: socket, address: Any) -> None:
        self.sock: socket = sock
        self.match_check: bool = False
        self.address: Any = address
        self.name: str = ""

    @property
    def state(self) -> bool:
        try:
            self.sock.send("".encode())
        except:
            return False
        return True

    def load(self, command_q: Queue[Any]) -> None:
        try:
            buff: str = self.sock.recv(2048).decode()
            for data in buff.split("\\"):
                if len(data) == 0:
                    continue
                try:
                    command_q.put(loads(data))
                except:
                    print(traceback.format_exc(), end="Invalid Data Type Conversion\n")
        except:
            ...
