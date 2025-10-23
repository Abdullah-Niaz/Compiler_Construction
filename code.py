import copy

# initial and goal states
initial = [[7, 2, 4],
           [5, 6, 0],
           [8, 1, 3]]

goal = [[6, 7, 8],
        [3, 4, 5],
        [0, 1, 2]]

# Manhattan distance heuristic


def manhattan(state):
    pos = {}
    for i in range(3):
        for j in range(3):
            pos[state[i][j]] = (i, j)
    dist = 0
    for i in range(3):
        for j in range(3):
            val = goal[i][j]
            if val != 0:
                x, y = pos[val]
                dist += abs(x - i) + abs(y - j)
    return dist

# find blank position


def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

# generate all neighbors


def get_neighbors(state):
    x, y = find_blank(state)
    moves = [(-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right")]
    res = []
    for dx, dy, mv in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = copy.deepcopy(state)
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            res.append((new_state, mv))
    return res

# Hill Climbing


def hill_climb(start):
    current = copy.deepcopy(start)
    current_h = manhattan(current)
    steps = [(copy.deepcopy(current), "Start", current_h)]

    while True:
        neighbors = get_neighbors(current)
        best_neighbor = None
        best_h = current_h

        for n, mv in neighbors:
            h = manhattan(n)
            if h < best_h:
                best_h = h
                best_neighbor = (n, mv)

        if best_neighbor is None:
            break

        current, move = best_neighbor
        current_h = best_h
        steps.append((copy.deepcopy(current), move, current_h))

        if current_h == 0:
            break

    return steps


steps = hill_climb(initial)

# show the steps
for i, (s, mv, h) in enumerate(steps):
    print(f"Step {i}: Move = {mv}, Heuristic = {h}")
    for row in s:
        print(" ", " ".join(str(x) if x != 0 else "_" for x in row))
    print()
