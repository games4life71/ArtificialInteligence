from ArtificialInteligence.lab1.src import modelState as ms
from ArtificialInteligence.lab2.src import greedy_model as gm
import time

heuristic_used = gm.compute_hammings_euristic

SMALL_INSTANCE = [2, 5, 3, 1, 0, 6, 4, 7, 8]
MEDIUM_INSTANCE = [8, 6, 7, 2, 5, 4, 0, 3, 1]
LARGE_INSTANCE = [2, 7, 5, 0, 8, 4, 3, 1, 6]

used_instance = SMALL_INSTANCE
used_instance_string = used_instance == SMALL_INSTANCE and "SMALL_INSTANCE" or used_instance == MEDIUM_INSTANCE and "MEDIUM_INSTANCE" or "LARGE_INSTANCE"


def test_greedy_model():
    start = time.time()
    solution = gm.greedy_algorithm(ms.ModelState(ms.transform_input(used_instance), None),
                                   heuristic_used)

    print("Time elapsed: ", time.time() - start, "seconds")
    # print(compute_manhattan_euristic([8, 6, 7, 2, 5, 4, 0, 3, 1]))
    if solution[0] is None:
        print("No solution found")
    else:
        ms.print_state(solution[0].state)
        print("Steps: ", solution[1])


    import os
    # print the current working directory

    os.chdir("D:\Projects\AI\ArtificialInteligence\\testing\output")
    # execute dir command

    file_name = "output_" + str(heuristic_used.__name__) + " " + used_instance_string + ".txt"
    output = open(file_name, "w")

    for move in gm.recorded_moves:
        # save the moves in a file

        for i in range(0, 3):
            for j in range(0, 3):
                output.write(str(move.state[i][j]) + " ")
            output.write("\n")

        output.write("\n")

    output.write("Time elapsed: " + str(time.time() - start) + "seconds")
    output.write("\n")
    output.write("Steps: " + str(solution[1]))


def test_idffs():
    max_depth = 25
    # test iddfs algorithm
    start_time = time.time()
    solution = ms.IDDFS(ms.ModelState(ms.transform_input(used_instance), None), max_depth)
    finish_time = time.time() - start_time
    file_name = "output_IDDFS_" + used_instance_string + ".txt"
    output = open(file_name, "w")
    if solution is None:
        output.write("No solution found")

    else:
        state = solution[0]
        output.write("Solution found at depth: " + str(solution[1]) + "\n")
        output.write("Time elapsed: " + str(finish_time) + "seconds\n")

        for i in range(0, 3):
            for j in range(0, 3):
                output.write(str(state.state[i][j]) + " ")
            output.write("\n")
        output.write("\n")

test_greedy_model()

# test_idffs()
