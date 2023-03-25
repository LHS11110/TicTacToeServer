from socket import socket, error as SocketError
from queue import Queue
from json import loads
from typing import Any
import traceback
import errno


class Player:
    def __init__(self, sock: socket, address: Any) -> None:
        self.sock: socket = sock
        self.match_check: bool = False
        self.address: Any = address
        self.name: str = ""
        self.buffs: list[str] = []

    @property
    def state(self) -> bool:
        try:
            msg: bytes = b""
            msg = self.sock.recv(2048)
            if len(msg) == 0:
                return False
            for m in msg.decode().split("\\"):
                if len(m) == 0:
                    continue
                self.buffs.append(m)
        except SocketError as error:
            if error.errno == errno.WSAECONNRESET:
                return False
        return True

    def load(self, command_q: Queue[Any]) -> None:
        try:
            buff: str = self.sock.recv(2048).decode()
            while len(self.buffs) != 0:
                try:
                    command_q.put(loads(self.buffs.pop()))
                except:
                    print(traceback.format_exc(), end="Invalid Data Type Conversion\n")
            for data in buff.split("\\"):
                if len(data) == 0:
                    continue
                try:
                    command: Any = loads(data)
                    command_q.put(command)
                except:
                    print(traceback.format_exc(), end="Invalid Data Type Conversion\n")
        except:
            ...
