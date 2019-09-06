import copy
import datetime

initial_graph = []
moves = []
dfs_level = 1
now = datetime.datetime.now()
dfs_durations = [now - now for i in range(8)]
print_grid_enable = True
move_count = 0


def get_inputs():
    for i in range(8):
        x, y = map(int, input().split(','))
        initial_graph.append((x, y))


def generate_moves(accuracy):
    for i in range(accuracy + 1):
        if i == 0:
            moves.append((0, 0))
        else:
            moves.append((-i, -i))
            moves.append((-i, 0))
            moves.append((-i, i))
            moves.append((0, -i))
            moves.append((0, i))
            moves.append((i, -i))
            moves.append((i, 0))
            moves.append((i, i))


def is_legal_move(x, y, dx, dy):
    if (x + dx) > 8 or (x + dx) < 1:
        return False
    if (y + dy) > 8 or (y + dy) < 1:
        return False
    return True


def dfs(graph, level):
    global move_count
    if is_graph_valid(graph):
        print_grid(graph, "Found")
        print_changes(graph)
        return True
    if level > dfs_level:
        return False
    x, y = graph[level]
    for move in moves:
        dx, dy = move
        if is_legal_move(x, y, dx, dy):
            move_count += 1
            new_graph = copy.deepcopy(graph)
            new_graph[level] = (x + dx, y + dy)
            has_found_answer = dfs(new_graph, level+1)
            if has_found_answer:
                return True
    return False


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


def print_durations():
    print("-- Durations --")
    for index, duration in enumerate(dfs_durations):
        print("deep", index + 1, "->", duration.total_seconds())
    duration_sum = sum(dfs_durations, datetime.timedelta())
    print("sum ->", duration_sum.total_seconds())


def main():
    global dfs_level
    get_inputs()
    print_grid(initial_graph, label="Graph")
    generate_moves(accuracy=1)
    has_found_answer = False
    while not has_found_answer and dfs_level < 8:
        start = datetime.datetime.now()
        print("searching at deep", dfs_level)

        has_found_answer = dfs(initial_graph, level=0)

        end = datetime.datetime.now()
        dfs_durations[dfs_level] = end - start
        print("duration:", dfs_durations[dfs_level].total_seconds())

        dfs_level += 1

    print_durations()
    print("move count:", move_count)


if __name__ == '__main__':
    main()
