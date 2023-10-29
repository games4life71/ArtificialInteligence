# define the table 9x9
from random import random
import copy

TABLE = [[0 for x in range(9)] for y in range(9)]

# -1 for grey empty cells even numbers
# 0 for white empty cells
SOLUTION = [[0 for x in range(9)] for y in range(9)]


def import_solution(problem_file_name):
    solution_file = open("instances/" + problem_file_name + "_solved.txt", "r")
    lines = solution_file.readlines()
    line_index = 0
    for line in lines:
        line = line.replace('\n', '')
        line = line.replace(' ', '')
        # print(line)
        for index in range(len(line)):
            SOLUTION[line_index][index] = int(line[index])
        line_index += 1


def compare_tables(table1, table2):
    for row in range(9):
        for column in range(9):
            if table1[row][column] != table2[row][column]:
                print("the tables are not equal", table1[row][column], table2[row][column])
                return False
    return True


INITAL_TABLE = [[0 for x in range(9)] for y in range(9)]


def generate_instance(problem_file_name, solved_file_name):
    problem = open("instances/" + problem_file_name + ".txt", "r")
    solved = open("instances/" + solved_file_name + ".txt", "r")
    problemLines = problem.readlines()
    solvedLines = solved.readlines()
    # read a line from both files while not finished
    line_index = 0
    for problemLine, solvedLine in zip(problemLines, solvedLines):
        # problemLine = problemLine.strip()
        problemLine = problemLine.replace('\n', '')
        problemLine = problemLine.replace(' ', '')
        solvedLine = solvedLine.replace('\n', '')
        solvedLine = solvedLine.replace(' ', '')

        for index in range(len(problemLine)):
            if problemLine[index] == "0":
                if int(solvedLine[index]) % 2 == 0:
                    TABLE[line_index][index] = -1
                    INITAL_TABLE[line_index][index] = -1
                else:
                    TABLE[line_index][index] = 0
                    INITAL_TABLE[line_index][index] = 0
            else:
                TABLE[line_index][index] = int(problemLine[index])
                INITAL_TABLE[line_index][index] = int(problemLine[index])

        line_index += 1


def printTable(table):
    for row in range(9):
        for column in range(9):
            print(table[row][column], end=" ")
        print()


def find_first_empty_cell(current_table):
    for row in range(9):
        for column in range(9):
            if current_table[row][column] == 0 or current_table[row][column] == -1:
                return row, column, current_table[row][column]
    return -1, -1, -9  # not found


# check if the table is valid
def consistent_value(current_table, row, column, value):
    return check_column(current_table, column, value) and check_row(current_table, row, value) and check_square(
        current_table, row, column, value)


def check_column(current_table, column, value):
    for i in range(9):
        if current_table[i][column] == value:
            return False
    return True


def check_row(current_table, row, value):
    for i in range(9):
        if current_table[row][i] == value:
            return False
    return True


def is_complete(current_table):
    for row in range(9):
        for column in range(9):
            if current_table[row][column] == 0 or current_table[row][column] == -1:
                return False
    return True


def check_square(current_table, row, column, value):
    # get the center of the square
    center_row = (row // 3) * 3 + 1
    center_column = (column // 3) * 3 + 1
    # for every directions
    for i in range(-1, 2):
        for j in range(-1, 2):
            if current_table[center_row + i][center_column + j] == value:
                return False
    return True


# generate a random sudoku table that is valid

def simple_backtrack(current_table):
    printTable(current_table)
    print()

    if is_complete(current_table):  #
        print("complete")
        return current_table

    next_row, next_column, cell_color = find_first_empty_cell(current_table)
    # print("next", next_row, next_column, cell_color)
    possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # the domain of the cell
    if cell_color == -1:
        possible_values = [2, 4, 6, 8]
    for value in possible_values:
        if consistent_value(current_table, next_row, next_column, value):
            current_table[next_row][next_column] = value
            result = simple_backtrack(current_table)
            if result is not None:
                # print("result", result)
                return result
            current_table[next_row][next_column] = cell_color
    return None


domains = [[[] for x in range(9)] for y in range(9)]


# init the domains of the cells
def init_domains(current_table):
    for row in range(9):
        for column in range(9):
            if current_table[row][column] == 0:
                domains[row][column] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            elif current_table[row][column] == -1:
                domains[row][column] = [2, 4, 6, 8]
            else:
                domains[row][column] = [current_table[row][column]]


def check_empty_domains(current_domains, current_table):
    for row in range(9):
        for column in range(9):
            if len(current_domains[row][column]) == 0 and current_table[row][column] <= 0:
                # print("empty domain found at ", row, column)
                return True
    return False


# update  of the cells in the same row, column and square
def update_domains(row, column, value, current_domains_param):
    # in the same row
    new_domain = copy.deepcopy(current_domains_param)

    # new_domain[row][column] = [value]
    for i in range(9):
        if value in new_domain[row][i] and INITAL_TABLE[row][i] <= 0:
            new_domain[row][i].remove(value)  # it also removes from the original list

    # in the same column
    for i in range(9):
        if value in new_domain[i][column] and INITAL_TABLE[i][column] <= 0:
            new_domain[i][column].remove(value)
        # in the same square
        # get the center of the square
    center_row = (row // 3) * 3 + 1
    center_column = (column // 3) * 3 + 1
    # for every directions
    for i in range(-1, 2):
        for j in range(-1, 2):
            if value in new_domain[center_row + i][center_column + j] and INITAL_TABLE[center_row + i][
                center_column + j] <= 0:
                new_domain[center_row + i][center_column + j].remove(value)
    return new_domain


def backtracking_with_forward_check(current_table, current_domains):
    printTable(current_table)
    print()

    if is_complete(current_table):  #
        # print("complete")
        return current_table

    next_row, next_column, cell_color = find_first_empty_cell(current_table)

    possible_values = current_domains[next_row][next_column]  # the domain of the cell
    # print("pos val", possible_values, "for cell ", next_row, next_column)

    for value in possible_values:
        #    print("trying value ", value, "for cell ", next_row, next_column)
        if consistent_value(current_table, next_row, next_column, value):
            # print("value fit ", value, "for cell ", next_row, next_column)
            # current_table[next_row][next_column] = value # update the table
            # make a new table
            new_table = copy.deepcopy(current_table)
            new_table[next_row][next_column] = value
            printTable(new_table)
            print()
            # update the domains

            new_domain = update_domains(next_row, next_column, value, current_domains)
            # print("current_domains", current_domains)
            # print()
            # print("new domain", new_domain)

            if not check_empty_domains(new_domain, new_table):

                result = backtracking_with_forward_check(new_table, new_domain)

                if result is not None:
                    # print("result", result)
                    return result

            # print("backtrack -- found empty domain")
            printTable(current_table)
            print()
            # current_table[next_row][next_column] = cell_color
            # # update the domains back
            # print("restoring value ", value, "for cell ", next_row, next_column)
            # restore_value_in_domains(next_row, next_column, value, new_domain)
            # print(current_domains, "current domains")
    return None


def backtracking_with_forward_checkMRV(current_table, current_domains):
    printTable(current_table)
    print()

    if is_complete(current_table):  #
        # print("complete")
        return current_table

    # next_row, next_column, cell_color = find_first_empty_cell(current_table)
    next_row,next_column,cell_color = find_first_empty_cell_mrv(current_table,current_domains)
    possible_values = current_domains[next_row][next_column]  # the domain of the cell
    # print("pos val", possible_values, "for cell ", next_row, next_column)

    for value in possible_values:
        #    print("trying value ", value, "for cell ", next_row, next_column)
        if consistent_value(current_table, next_row, next_column, value):
            # print("value fit ", value, "for cell ", next_row, next_column)
            # current_table[next_row][next_column] = value # update the table
            # make a new table
            new_table = copy.deepcopy(current_table)
            new_table[next_row][next_column] = value
            printTable(new_table)
            print()
            # update the domains

            new_domain = update_domains(next_row, next_column, value, current_domains)
            # print("current_domains", current_domains)
            # print()
            # print("new domain", new_domain)

            if not check_empty_domains(new_domain, new_table):

                result = backtracking_with_forward_check(new_table, new_domain)

                if result is not None:
                    # print("result", result)
                    return result

            # print("backtrack -- found empty domain")
            printTable(current_table)
            print()
            # current_table[next_row][next_column] = cell_color
            # # update the domains back
            # print("restoring value ", value, "for cell ", next_row, next_column)
            # restore_value_in_domains(next_row, next_column, value, new_domain)
            # print(current_domains, "current domains")
    return None


# implement MRV heuristic for choosing the next cell to fill

def find_first_empty_cell_mrv(current_table, current_domains):
    min_domain = 10
    min_row = -1
    min_column = -1
    for row in range(9):
        for column in range(9):
            if current_table[row][column] == 0 or current_table[row][column] == -1:
                if len(current_domains[row][column]) < min_domain:
                    min_domain = len(current_domains[row][column])
                    min_row = row
                    min_column = column
    return min_row, min_column, current_table[min_row][min_column]


generate_instance("instance1", "instance1_solved")
# printTable(TABLE)
print()
init_domains(TABLE)
my_solution = backtracking_with_forward_checkMRV(TABLE, domains)
# printTable(TABLE)

import_solution("instance1")
# printTable(SOLUTION)
print(compare_tables(my_solution, SOLUTION))
