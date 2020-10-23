import heapq
import time

lines = 3
column = 3


class Node:
    heuristic = -1
    distance = -1
    state = []
    predecessor = None

    def __init__(self, p_heuristic, p_distance, p_state, p_pred):
        self.heuristic = p_heuristic
        self.distance = p_distance
        self.state = p_state
        self.predecessor = p_pred

    def __lt__(self, other):
        if (self.heuristic + self.distance) != (other.heuristic + other.distance):
            return (self.heuristic + self.distance) < (other.heuristic + other.distance)
        else:
            return self.heuristic < other.heuristic

    def print_state(self):
        global lines
        global column
        for i in range(0, lines):
            for j in range(0, column):
                if self.state[i][j] == -1:
                    print('  _', end='')
                else:
                    print('{:3d}'.format(self.state[i][j]), end='')
            print()


def num_of_inversions(p_state):
    stack = []
    sum = 0

    for i_l in range(0, lines):
        for j_c in range(0, column):
            if p_state[i_l][j_c] != -1:
                stack.append(p_state[i_l][j_c])

    for i in range(0, len(stack)):
        for j in range(i + 1, len(stack)):
            if stack[i] > stack[j]:
                sum += 1
    return sum


# spytat sa na cviceni
def is_possible(p_state):
    sum = num_of_inversions(p_state)
    global column
    global lines
    if column % 2 == 1:
        if sum % 2 == 0:
            return True
        else:
            return False
    else:
        line, col = find_blank(p_state)
        if lines - line % 2 == 1 and sum % 2 == 0:
            return True
        elif lines - line % 2 == 0 and sum % 2 == 1:
            return True
        else:
            return False




def heuristic_1(p_start_state, p_final_state):
    heu = 0
    global lines
    global column
    for i_l in range(0, lines):
        for j_c in range(0, column):
            if p_start_state[i_l][j_c] != p_final_state[i_l][j_c]:
                heu += 1
    return heu


def find(value, p_state):
    for i_l in range(0, lines):
        for j_c in range(0, column):
            if value == p_state[i_l][j_c]:
                return i_l, j_c


def heuristic_2(p_start_state, p_final_state):
    heu = 0
    global lines
    global column
    for i_l in range(0, lines):
        for j_c in range(0, column):
            x_l, y_c = find(p_start_state[i_l][j_c], p_final_state)
            heu += abs(i_l-x_l) + abs(j_c-y_c)
    return heu


def load_state_from_console():
    global lines
    global column
    print("Zadaj ", column*lines - 1," čísel a m pre prázdne políčko: ", end='')
    res = []
    x = list(input().split())
    for i_l in range(0, lines):
        res.append([])
        for j_c in range(0, column):
            if x[i_l * column + j_c] == 'm':
                res[i_l].append(-1)
            else:
                res[i_l].append(int(x[i_l * column + j_c]))
    return res


def find_blank(p_state):
    global lines
    global column
    for i_l in range(0, lines):
        for j_c in range(0, column):
            if p_state[i_l][j_c] == -1:
                return i_l, j_c


def swap(x1_l, y1_c, x2_l, y2_c, p_state):
    temp = p_state[x1_l][y1_c]
    p_state[x1_l][y1_c] = p_state[x2_l][y2_c]
    p_state[x2_l][y2_c] = temp


def print_process(node):
    steps = []
    while node.predecessor != None:
        steps.insert(0, node)
        node = node.predecessor
    steps.insert(0, node)

    for x in steps:
        x.print_state()
        print()


def find_final(start_pos, final_pos):
    heap = []
    first = Node(heuristic_1(start_pos, final_pos), 0, start_pos, None)
    created = {}
    while first.heuristic != 0:
        x_l, y_c = find_blank(first.state)

        # right shift
        if y_c - 1 >= 0:
            new = [list(x) for x in first.state]
            swap(x_l, y_c - 1, x_l, y_c, new)
            if created.get(hash(str(new))) != new:
                created[hash(str(new))] = new
                heapq.heappush(heap, Node(heuristic_2(new, final_pos), first.distance + 1, new, first))

        # left shift
        if y_c + 1 < column:
            new = [list(x) for x in first.state]
            swap(x_l, y_c + 1, x_l, y_c, new)
            if created.get(hash(str(new))) != new:
                created[hash(str(new))] = new
                heapq.heappush(heap, Node(heuristic_2(new, final_pos), first.distance + 1, new, first))

        # up shift
        if x_l + 1 < lines:
            new = [list(x) for x in first.state]
            swap(x_l + 1, y_c, x_l, y_c, new)
            if created.get(hash(str(new))) != new:
                created[hash(str(new))] = new
                heapq.heappush(heap, Node(heuristic_2(new, final_pos), first.distance + 1, new, first))

        # down shift
        if x_l - 1 >= 0:
            new = [list(x) for x in first.state]
            swap(x_l - 1, y_c, x_l, y_c, new)
            if created.get(hash(str(new))) != new:
                created[hash(str(new))] = new
                heapq.heappush(heap, Node(heuristic_2(new, final_pos), first.distance + 1, new, first))

        first = heapq.heappop(heap)
    return first


lines = int(input("Zadaj počet riadkov: "))
column = int(input("Zadaj počet stĺpcov: "))
start_pos = load_state_from_console()
final_pos = load_state_from_console()
timer = 0.0
"""
for i in range(0, 100):
    start = time.time()
    print_process(find_final(start_pos, final_pos))
    end = time.time()
    timer += end - start
print("Cas: ", timer/100)

"""
if is_possible(start_pos) == is_possible(final_pos):
    print("Je mozne")
    start = time.time()
    print_process(find_final(start_pos, final_pos))
    end = time.time()
    print("Cas: ", end - start)
else:
    print("Nie je mozne")