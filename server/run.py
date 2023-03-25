from system.main import TicTacToeServer, Config
import os


def _main() -> None:
    serv: TicTacToeServer = TicTacToeServer()
    ip: str = str(os.getenv("IP"))
    port: str = str(os.getenv("PORT"))
    if ip == "None" or port == "None":
        return
    config: Config = Config(IP=ip, PORT=int(port), backlog=20, number_of_room=10000)
    serv.setting(config=config)

    while True:
        serv.update()


if __name__ == "__main__":
    _main()
