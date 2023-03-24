from system.main import TicTacToeServer

serv: TicTacToeServer = TicTacToeServer()
serv.setting()

while True:
    serv.update()
