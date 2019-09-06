import copy
import datetime

initial_graph = []
moves = []

astar_matched = []
astar_cost = []
astar_pioneers = []
astar_pioneers_moves_count = []
astar_pioneers_total_costs = []

print_grid_enable = True
counts = 0


def get_inputs():
    for i in range(8):
        x, y = map(int, input().split(','))
        initial_graph.append((x, y))


def generate_moves():
    moves.append((-1, -1))
    moves.append((-1, 0))
    moves.append((-1, 1))
    moves.append((0, -1))
    moves.append((0, 1))
    moves.append((1, -1))
    moves.append((1, 0))
    moves.append((1, 1))


def is_legal_move(x, y, dx, dy):
    if (x + dx) > 8 or (x + dx) < 1:
        return False
    if (y + dy) > 8 or (y + dy) < 1:
        return False
    return True


def is_graph_valid(graph):
    for i, (x, y) in enumerate(graph):
        for j in range(i + 1, 8):
            xj, yj = graph[j]
            if xj == x or yj == y or abs(x - xj) == abs(y - yj):
                return False
    return True


def print_grid(graph, label=None):
    if label is not None:
        print("-" * 4, label, "-" * 4)
    if not print_grid_enable:
        return
    lines = [["O" for i in range(8)] for j in range(8)]
    for (x, y) in graph:
        lines[x - 1][y - 1] = "X"
    for line in lines:
        print(" ".join(line))


def print_changes(graph):
    print("--- Changes ---")
    for i, (x, y) in enumerate(initial_graph):
        xn, yn = graph[i]
        print('(', x - xn, ',', y - yn, ')')


def a_star():
    global counts
    while True:
        counts += 1
        best_total_cost = min(astar_pioneers_total_costs)
        best_index = astar_pioneers_total_costs.index(best_total_cost)
        move_count = astar_pioneers_moves_count[best_index]
        new_graph = astar_pioneers[best_index]

        if is_graph_valid(new_graph):
            return new_graph

        # print_grid(new_graph, "best")
        print("move:", move_count, "threats:", (best_total_cost - move_count) // 2, "cost:", best_total_cost)
        astar_matched.append(new_graph)
        astar_cost.append((move_count, best_total_cost))

        astar_pioneers.pop(best_index)
        astar_pioneers_moves_count.pop(best_index)
        astar_pioneers_total_costs.pop(best_index)

        add_pioneers(new_graph, move_count)


def add_pioneers(graph, cost):
    for level, (x, y) in enumerate(graph):
        for index, (dx, dy) in enumerate(moves):
            if is_legal_move(x, y, dx, dy):
                new_graph = copy.deepcopy(graph)
                new_graph[level] = (x + dx, y + dy)
                if new_graph in astar_matched:
                    continue
                threat_count = get_threats_count(new_graph)
                astar_pioneers.append(new_graph)
                astar_pioneers_moves_count.append(cost + 1)
                astar_pioneers_total_costs.append(2 * threat_count + cost + 1)


def get_threats_count(graph):
    threat_counts = 0
    for i, (x, y) in enumerate(graph):
        for j in range(i + 1, 8):
            xj, yj = graph[j]
            if xj == x or yj == y or abs(x - xj) == abs(y - yj):
                threat_counts += 1
    return threat_counts


def main():
    global astar_matched, astar_cost
    get_inputs()
    print_grid(initial_graph, label="Graph")
    print("initial threats:", get_threats_count(initial_graph))
    generate_moves()

    start = datetime.datetime.now()
    astar_matched = [initial_graph]
    astar_cost = [(0, 0)]
    add_pioneers(initial_graph, 0)

    graph = a_star()
    end = datetime.datetime.now()

    print_grid(graph, label="Found")
    print_changes(graph)
    print("duration:", (end - start).total_seconds())
    print("move count:", counts)


if __name__ == '__main__':
    main()
