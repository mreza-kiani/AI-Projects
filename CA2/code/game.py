from RandomMinimaxAgent import RandomMinimaxAgent
from agent import Agent
from board import Board
from cliBoard import CliBoard
from graphicalBoard import GraphicalBoard


def switchTurn(turn):
    if turn == 'W':
        return 'B'
    return 'W'


def play(white, black, board):
    # graphicalBoard = GraphicalBoard(board)
    cliBoard = CliBoard(board)
    turn = 'W'
    while not board.finishedGame():
        if turn == 'W':
            from_cell, to_cell = white.move(board)
        elif turn == 'B':
            from_cell, to_cell = black.move(board)
        else:
            raise Exception
        board.changePieceLocation(turn, from_cell, to_cell)
        cliBoard.showBoard(label=turn)
        turn = switchTurn(turn)
        # graphicalBoard.showBoard()

    if board.win('B'):
        print('B Wins')
    else:
        print('A Wins')


if __name__ == '__main__':
    board = Board(6, 6, 2)
    white = RandomMinimaxAgent('W', 'B')
    # white = Agent('W', 'B', strategy="Custom", height=4)
    # white = Agent('W', 'B', strategy="Defensive", height=4)
    you = Agent('B', 'W', strategy="Aggressive")
    play(white, you, board)
