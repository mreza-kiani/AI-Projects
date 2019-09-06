import datetime

from alphaBetaPruning import AlphaBetaPruning
from myTree import MyTree


class Agent:
    def __init__(self, my_color, opponent_color, strategy="Defensive", height=4, time=None):
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.strategy = strategy
        self.height = height
        self.time = time

    def move(self, board):
        start = datetime.datetime.now()

        game_tree = MyTree(board, self.my_color, self.opponent_color, self.height)
        from_cell, to_cell = AlphaBetaPruning.cal_next_move(game_tree, self.height, self.my_color, self.strategy)

        end = datetime.datetime.now()
        print("step time: {}".format((end-start).total_seconds()))

        return from_cell, to_cell
