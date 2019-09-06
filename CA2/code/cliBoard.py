class CliBoard:
    def __init__(self, board):
        self.board = board
        self.showBoard("Init")

    def showBoard(self, label):
        self.board.print(label)
