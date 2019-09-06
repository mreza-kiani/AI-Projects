import math


class AlphaBetaPruning:
    @staticmethod
    def cal_next_move(tree, height, color, strategy):
        AlphaBetaPruning.compute_minimax_value(tree.root, color, 1, height, -math.inf, math.inf, strategy)
        decision_node = tree.root.getDecisionChild()
        return decision_node.getFromCell(), decision_node.getToCell()

    @staticmethod
    def compute_minimax_value(root_node, color, height, max_height, alpha, beta, strategy):
        is_max = True
        if height % 2 == 0:
            is_max = False

        max_min_utility = -math.inf if is_max else math.inf
        decision_node = None

        for child in root_node.children:
            if height == max_height:
                AlphaBetaPruning.compute_value(root_node, color, strategy)
            else:
                AlphaBetaPruning.compute_minimax_value(child, color, height + 1, max_height, alpha, beta, strategy)

            if is_max:
                if child.utility > max_min_utility:
                    max_min_utility = child.utility
                    decision_node = child
                    if child.utility > alpha:
                        alpha = child.utility
                elif child.utility < alpha:
                    break
            else:
                if child.utility < max_min_utility:
                    max_min_utility = child.utility
                    decision_node = child
                    if child.utility < beta:
                        beta = child.utility
                elif child.utility > beta:
                    break

            root_node.setUtility(max_min_utility)
            root_node.setDecisionChild(decision_node)

    @staticmethod
    def compute_value(node, color, strategy):
        if strategy == "Defensive":
            node.setDefensiveEvaluationFunction(color)
        elif strategy == "Aggressive":
            node.setAggressiveEvaluationFunction(color)
        else:
            node.setCustomEvaluationFunction(color)
