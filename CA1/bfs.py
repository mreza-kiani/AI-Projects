import copy
import datetime

initial_graph = []
bfs_moves = []
queue = [[] for i in range(8)]
now = datetime.datetime.now()
bfs_durations = [now - now for i in range(8)]
print_grid_enable = True
move_count = 0


def get_inputs():
    for i in range(8):
        x, y = map(int, input().split(','))
        initial_graph.append((x, y))


def generate_bfs_moves(accuracy):
    for i in range(accuracy + 1):
        if i == 0:
            bfs_moves.append((0, 0))
        else:
            bfs_moves.append((-i, -i))
            bfs_moves.append((-i, 0))
            bfs_moves.append((-i, i))
            bfs_moves.append((0, -i))
            bfs_moves.append((0, i))
            bfs_moves.append((i, -i))
            bfs_moves.append((i, 0))
            bfs_moves.append((i, i))


def is_legal_move(x, y, dx, dy):
    if (x + dx) > 8 or (x + dx) < 1:
        return False
    if (y + dy) > 8 or (y + dy) < 1:
        return False
    return True


def bfs():
    global move_count
    for level in range(8):
        start = datetime.datetime.now()
        print("level {} started".format(level))
        while len(queue[level]) != 0:
            graph = queue[level].pop(0)
            x, y = initial_graph[level]
            # print_grid(graph, label="base in level {} & queue len {}".format(level, len(queue[level])))

            for bfs_move in bfs_moves:
                dx, dy = bfs_move
                if is_legal_move(x, y, dx, dy):
                    move_count += 1
                    new_graph = copy.deepcopy(graph)
                    new_graph[level] = (x + dx, y + dy)
                    # print_grid(new_graph, label="change for {}".format((dx, dy)))
                    if is_graph_valid(new_graph):
                        print("ended")
                        end = datetime.datetime.now()
                        bfs_durations[level] = end - start
                        print("duration:", bfs_durations[level].total_seconds())

                        print_grid(new_graph, label="Found")
                        print_changes(new_graph)
                        print("move count:", move_count)
                        return
                    if level != 7:
                        queue[level + 1].append(new_graph)
        print("ended")
        end = datetime.datetime.now()
        bfs_durations[level] = end - start
        print("duration:", bfs_durations[level].total_seconds())


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
    for x, y in graph:
        lines[x - 1][y - 1] = "X"
    for line in lines:
        print(" ".join(line))


def print_changes(graph):
    print("--- Changes ---")
    for i, (x, y) in enumerate(initial_graph):
        xn, yn = graph[i]
        print('(', x - xn, ',', y - yn, ')')


def print_durations():
    print("-- Durations --")
    for index, duration in enumerate(bfs_durations):
        print(index + 1, "->", duration.total_seconds())
    duration_sum = sum(bfs_durations, datetime.timedelta())
    print("sum ->", duration_sum.total_seconds())


def main():
    get_inputs()
    print_grid(initial_graph, "Graph")
    generate_bfs_moves(1)
    queue[0].append(initial_graph)
    bfs()
    print_durations()


if __name__ == '__main__':
    main()
