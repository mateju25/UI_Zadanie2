import heapq
import time

# vyska a sirka hlavolamu
lines = 3
column = 3
# typ heuristiky
type_heu = 1


# objekt uzla v grafe, obsahuje heuristiku, vzdialenost, stav a odkaz na predchodcu
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

    # metoda, podla ktorej heap porovnava stavy (najskor usporaduva podla suctu heuristiky a vzdialenosti a ak su
    # rovnake tak este ich usporiada na zaklade heuristiky)
    def __lt__(self, other):
        if (self.heuristic + self.distance) != (other.heuristic + other.distance):
            return (self.heuristic + self.distance) < (other.heuristic + other.distance)
        else:
            return self.heuristic < other.heuristic


# vyrata pocet inverzii v stave
def num_of_inversions(p_state):
    stack = []
    sum = 0
    # vyrobim si z dvojrozmerneho pola jednorozmerne
    for i_l in range(0, lines):
        for j_c in range(0, column):
            if p_state[i_l][j_c] != -1:
                stack.append(p_state[i_l][j_c])

    # zratam inverzie
    for i in range(0, len(stack)):
        for j in range(i + 1, len(stack)):
            if stack[i] > stack[j]:
                sum += 1
    return sum


# zisti, ci dany stav sa da usporiadat na stav (1 2 3 ...)
def is_possible(p_state):
    sum = num_of_inversions(p_state)
    global column
    global lines
    # sirka je parna
    if column % 2 == 1:
        # inverzie su parne
        if sum % 2 == 0:
            return True
        else:
            return False
    else:
        line, col = find_blank(p_state)
        # riadok prazdneho miesta zospodu je neparny a inverzie su parne
        if lines - line % 2 == 1 and sum % 2 == 0:
            return True
        # riadok prazdneho miesta zospodu je parny a inverzie su neparne
        elif lines - line % 2 == 0 and sum % 2 == 1:
            return True
        else:
            return False


# vyber typ heuristiky
def choose_heuristic(p_start_state, p_final_state):
    global type_heu
    if type_heu == 1:
        return heuristic_1(p_start_state, p_final_state)
    elif type_heu == 2:
        return heuristic_2(p_start_state, p_final_state)


# heuristika 1 - pocet policok na nespravnom mieste
def heuristic_1(p_start_state, p_final_state):
    heu = 0
    global lines
    global column
    for i_l in range(0, lines):
        for j_c in range(0, column):
            if p_start_state[i_l][j_c] != p_final_state[i_l][j_c]:
                heu += 1
    return heu


# najde poziciu danej hodnoty v stave (pouziva sa pri heuristike 2)
def find(p_value, p_state):
    for i_l in range(0, lines):
        for j_c in range(0, column):
            if p_value == p_state[i_l][j_c]:
                return i_l, j_c


# heuristika 2 - sucet vzdialenosti hodnot od svojho miesta
def heuristic_2(p_start_state, p_final_state):
    heu = 0
    global lines
    global column
    for i_l in range(0, lines):
        for j_c in range(0, column):
            x_l, y_c = find(p_start_state[i_l][j_c], p_final_state)
            heu += abs(i_l-x_l) + abs(j_c-y_c)
    return heu


# nacita sekvenciu cisel a m do 2d pola
def create_state_from_string(p_input):
    global lines
    global column
    res = []
    x = list(p_input.split())
    for i_l in range(0, lines):
        res.append([])
        for j_c in range(0, column):
            if x[i_l * column + j_c] == 'm':
                res[i_l].append(-1)
            else:
                res[i_l].append(int(x[i_l * column + j_c]))
    return res


# nacita vstup zo suboru
def load_states_from_file(p_filename):
    global lines
    global column
    file = open(p_filename, "r").read().split('\n')
    lines = int(file[0])
    column = int(file[1])
    start = file[2]
    final = file[3]
    return create_state_from_string(start), create_state_from_string(final)


# najde prazdne miesto v stave
def find_blank(p_state):
    global lines
    global column
    for i_l in range(0, lines):
        for j_c in range(0, column):
            if p_state[i_l][j_c] == -1:
                return i_l, j_c


# vymeni dve hodnoty v stave
def swap(x1_l, y1_c, x2_l, y2_c, p_state):
    temp = p_state[x1_l][y1_c]
    p_state[x1_l][y1_c] = p_state[x2_l][y2_c]
    p_state[x2_l][y2_c] = temp


# vypise sekvenciu operatorov
def print_process(p_node):
    steps = []
    # prevratim poradie
    while p_node.predecessor is not None:
        steps.insert(0, p_node)
        p_node = p_node.predecessor
    steps.insert(0, p_node)

    # zistujem rozdiel a vypisem operatory
    for x in range(0, len(steps)-1):
        x1, y1 = find_blank(steps[x].state)
        x2, y2 = find_blank(steps[x+1].state)
        if x1 - 1 == x2:
            print("DOLE, ", end='')
        if x1 + 1 == x2:
            print("HORE, ", end='')
        if y1 - 1 == y2:
            print("VPRAVO, ", end='')
        if y1 + 1 == y2:
            print("VĽAVO, ", end='')
        #steps[x].print_state()
    print()


# A* algoritmus - vytvorim si min_heap, kde ukladam vytvorene uzly, vyberiem vzdy najmensi prvok a rozbalim ho do
# dalsich stavov, vsetky vytvorene stavy pridam do hash tabulky, aby som sa necyklil
def find_final(p_start_pos, p_final_pos):
    heap = []
    first = Node(heuristic_1(p_start_pos, p_final_pos), 0, p_start_pos, None)
    created = {}
    while first.heuristic != 0:
        x_l, y_c = find_blank(first.state)

        # right shift
        if y_c - 1 >= 0:
            new = [list(x) for x in first.state]
            swap(x_l, y_c - 1, x_l, y_c, new)
            if created.get(hash(str(new))) != new:
                created[hash(str(new))] = new
                heapq.heappush(heap, Node(heuristic_2(new, p_final_pos), first.distance + 1, new, first))

        # left shift
        if y_c + 1 < column:
            new = [list(x) for x in first.state]
            swap(x_l, y_c + 1, x_l, y_c, new)
            if created.get(hash(str(new))) != new:
                created[hash(str(new))] = new
                heapq.heappush(heap, Node(heuristic_2(new, p_final_pos), first.distance + 1, new, first))

        # up shift
        if x_l + 1 < lines:
            new = [list(x) for x in first.state]
            swap(x_l + 1, y_c, x_l, y_c, new)
            if created.get(hash(str(new))) != new:
                created[hash(str(new))] = new
                heapq.heappush(heap, Node(heuristic_2(new, p_final_pos), first.distance + 1, new, first))

        # down shift
        if x_l - 1 >= 0:
            new = [list(x) for x in first.state]
            swap(x_l - 1, y_c, x_l, y_c, new)
            if created.get(hash(str(new))) != new:
                created[hash(str(new))] = new
                heapq.heappush(heap, Node(heuristic_2(new, p_final_pos), first.distance + 1, new, first))

        first = heapq.heappop(heap)
    return first


# vypise menu a ovladanie programu
def menu():
    global lines, column, type_heu
    print()
    print("*****************************************************************************")
    print("                          Riešiteľ  8 - hlavolamu                            ")
    print("                           Autor: Matej Delinčák                             ")
    print("*****************************************************************************")
    print()
    file = input("Nacitat zo suboru? y/n: ")
    if file == 'y':
        filename = input("Názov súboru: ")
    else:
        menu = input("Chceš riešiť 8-hlavolam? y/ine: ")
        if menu != 'y':
            lines = int(input("Zadaj počet riadkov: "))
            column = int(input("Zadaj počet stĺpcov: "))

    print("Vyber si heuristiku: ")
    print("1. Počet políčok, ktoré nie sú na svojom mieste")
    print("2. Súčet vzdialeností jednotlivých políčok od ich cieľovej pozície")
    type_heu = input("Možnosť: ")
    menu = int(input("Koľko razy chceš zopakovať riešenie? Zadaj číslo: "))

    if file == 'y':
        start_pos, final_pos = load_states_from_file(filename)
    else:
        print("Zadaj", column * lines - 1, "čísel a m pre prázdne políčko: ", end='')
        start_pos = create_state_from_string(input())
        print("Zadaj", column * lines - 1, "čísel a m pre prázdne políčko: ", end='')
        final_pos = create_state_from_string(input())

    timer = 0.0

    if is_possible(start_pos) == is_possible(final_pos):
        print("Riešenie je možné.")
        for i in range(0, menu):
            start = time.time()
            if menu > 1:
                find_final(start_pos, final_pos)
            else:
                print("Postupnosť: ")
                print_process(find_final(start_pos, final_pos))
            end = time.time()
            timer += end - start
        print("Cas: ", timer / menu)
    else:
        print("Riešenie nie je možné.")


menu()