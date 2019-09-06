import copy

from myNode import MyNode
from tree import Tree


class MyTree(Tree):
    def makeNode(self, height, board, from_cell=None, to_cell=None):
        node = MyNode(from_cell, to_cell, board)
        self.nodes[height].append(node)
        return node

    # def makeMinimaxChildrenFor(self, nodes, color, opponent_color, height):
    #     result_nodes = []
    #     for node in nodes:
    #         if node.board.win(color):
    #             node.utility = 100
    #             continue
    #         elif node.board.win(opponent_color):
    #             node.utility = -100
    #             continue
    #         else:
    #             pieces_from_cell, pieces_to_cell = node.board.getPiecesPossibleLocations(color)
    #             for i in range(len(pieces_to_cell)):
    #                 for j in range(len(pieces_to_cell[i])):
    #                     new_board = copy.deepcopy(node.board)
    #                     new_board.changePieceLocation(color, pieces_from_cell[i], pieces_to_cell[i][j])
    #
    #                     child_node = self.makeNode(height, new_board, pieces_from_cell[i], pieces_to_cell[i][j])
    #                     result_nodes.append(child_node)
    #
    #                     node.setChild(child_node)
    #
    #     return result_nodes
