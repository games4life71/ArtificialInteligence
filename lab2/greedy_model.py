from ArtificialInteligence.lab1.src import modelState as ms


# generate all the possible end states
def generate_final_states():
    final_states = []
    first_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    final_states.append(ms.transform_input(first_state.copy()))
    for i in range(0, 8):
        temp = first_state[i]
        first_state[i] = first_state[i + 1]
        first_state[i + 1] = temp
        final_array = ms.transform_input(first_state)
        final_states.append(final_array.copy())

    return final_states


# compute the manhattan distance between two points
# compute_manhattan_distance = lambda x, y: abs(x[0] - y[0]) + abs(x[1] - y[1])
def compute_manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


FINAL_STATES = generate_final_states()


def compute_manhattan_euristic(state):
    distance = 0
    # print(type(state),"tipul")
    for final_state in FINAL_STATES:
        distance += compute_manhattan2states(state, final_state)
    return distance / 9


def get_coords(state, element):
    for i in range(0, 3):
        for j in range(0, 3):
            if state[i][j] == element:
                return i, j


def compute_manhattan2states(mystate, final_state):
    distance = 0
    for i in range(0, 3):
        for j in range(0, 3):
            x1, y1 = get_coords(mystate, mystate[i][j])
            x2, y2 = get_coords(final_state, mystate[i][j])
            distance += compute_manhattan_distance((x1, y1), (x2, y2))

    return distance


def compute_hammings2states(state, final_state):
    #compute the number of elements that are not in the right position
    distance = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if state[i][j] != final_state[i][j]:
                distance += 1
    return distance


def compute_hammings_euristic(state):
    distance = 0
    for final_state in FINAL_STATES:
        distance += compute_hammings2states(state, final_state)
    return distance / 9

# print(compute_manhattan_euristic([1, 2, 3, 4, 5, 6, 7, 8, 0]))
from queue import PriorityQueue


def greedy_algorithm(init_state, heuristic):
    pq = PriorityQueue()
    heuristic_value = heuristic(init_state.state)
    pq.put((heuristic_value, init_state))
    visited = [init_state]
    steps = 0
    while not pq.empty():
        # get the state with the lowest heuristic
        value = pq.get()
        state = value[1]
        steps += 1
        # copy_state = state
        # print("type",type(copy_state))
        # state = pq.get()[1]  # get the state with the lowest heuristic
        # print(type(state),"tipulstate")
        if ms.check_final_state(state):
            return state,steps

        possible_moves_array = ms.possible_moves(state)
        # print(possible_moves_array, "possible moves")

        for move in possible_moves_array:

            zero_pos = state.get_zero_pos()

            try:
                # print(state.state, "state")
                new_state = ms.transition_move(state, move, zero_pos)
                # print(new_state.state, "new state")
            except Exception as e:
                print(e)
                continue

            if new_state not in visited:
                visited.append(new_state)
                heuristic_value = heuristic(new_state.state)
                # print(heuristic_value, "heuristic value")
                # print(heuristic_value, "heuristic value")
                # print("type new state", type(new_state))
                pq.put((heuristic_value, new_state))

    return None

import time
start = time.time()
solution = greedy_algorithm(ms.ModelState(ms.transform_input([7, 4, 1, 3, 2, 5, 0, 6, 8]), None),
                           compute_hammings_euristic)
print("Time elapsed: ", time.time() - start, "seconds")
# print(compute_manhattan_euristic([8, 6, 7, 2, 5, 4, 0, 3, 1]))
if solution[0] is None:
    print("No solution found")
else:
   ms.print_state(solution[0].state)
   print("Steps: ",solution[1])



