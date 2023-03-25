from typing import TYPE_CHECKING, Any, Union
import time

if TYPE_CHECKING:
    from player_info.player import Player


class Room:
    def __init__(self, rule: Any, players: list["Player"]) -> None:
        self.game: rule = rule(players)
        self.info: dict[str, Union[str, int]] = {
            "time": time.strftime("%Y.%m.%d - %H:%M:%S"),
            "rule_name": rule.__name__,
            "headcount": len(players),
        }

    def close(self) -> None:
        try:
            self.game.close()
        except:
            raise Exception(f"{self.info}\nclose() Method Not Found")

    def update(self) -> None:
        self.game.update()

    @property
    def end_check(self) -> bool:
        return self.game.end
