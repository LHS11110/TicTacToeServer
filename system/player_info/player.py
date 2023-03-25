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
        self.buffs: str = ""

    @property
    def state(self) -> bool:
        try:
            msg: bytes = b""
            msg = self.sock.recv(2048)
            if len(msg) == 0:
                return False
            self.buffs += msg.decode()
        except SocketError as error:
            if error.errno != errno.EWOULDBLOCK:
                print("Socket Error: ", error.errno)
                return False
        return True

    def load(self, command_q: Queue[Any]) -> None:
        try:
            buff: str = self.buffs
            self.buffs = ""
            try:
                buff += self.sock.recv(2048).decode()
            except:
                ...
            if len(buff) == 0:
                return
            for data in buff.split("\\"):
                if len(data) == 0:
                    continue
                try:
                    command: Any = loads(data)
                    command_q.put(command)
                except:
                    print(
                        traceback.format_exc() + data,
                        end="Invalid Data Type Conversion\n",
                    )
        except:
            ...
