from random import randint

from node import Node


class MyNode(Node):
    def setDefensiveEvaluationFunction(self, color):
        nodes = self.board.travelOverBoard(color)
        self.utility = 2 * len(nodes) + randint(-1, 1)

    def setAggressiveEvaluationFunction(self, color):
        opponent_color = "W" if color == "B" else "B"
        nodes = self.board.travelOverBoard(opponent_color)
        self.utility = 2 * (30 - len(nodes)) + randint(-1, 1)
        # self.board.print(label="uf: {}".format(self.utility))

    def setCustomEvaluationFunction(self, color):
        w_nodes = self.board.travelOverBoard("W")
        b_nodes = self.board.travelOverBoard("B")

        w_scores = 0
        for (x, y) in w_nodes:
            w_scores += (x - 1)
            if x == 5:
                w_scores += 50
        b_scores = 0
        for (x, y) in b_nodes:
            b_scores += (4 - x)
            if x == 0:
                b_scores += 50

        self.utility = (b_scores - w_scores) + (len(b_nodes) - len(w_nodes))
        if color == "W":
            self.utility *= -1
        # self.board.print(label="uf: {}".format(self.utility))
