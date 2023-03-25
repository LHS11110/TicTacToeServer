from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from player_info.player import Player


class MatchMaking:
    def __init__(self, headcount: int) -> None:
        self.headcount: int = headcount
        self.player_list: List["Player"] = []

    def push(self, player: "Player") -> None:
        if player.state:
            self.player_list.append(player)

    def match(self) -> List["Player"]:
        result: List["Player"] = []
        while (
            len(self.player_list) + len(result) >= self.headcount
            and len(result) < self.headcount
        ):
            player: "Player" = self.player_list.pop()
            if player.state:
                result.append(player)
            else:
                print("Close Socket")
        if len(result) < self.headcount:
            for p in result:
                self.player_list.append(p)
            return []
        else:
            return result
