import copy
import math

choices = [2, 7, 6, 9, 5, 1, 4, 3, 8]
INDEXES = [2, 7, 6, 9, 5, 1, 4, 3, 8]
TABLE = [[0 for x in range(3)] for y in range(3)]


# gets the position of a number in a 3x3 table
def get_3x3_pos(number):
    return INDEXES.index(number) // 3, INDEXES.index(number) % 3


def verify_win(player, current_table):

    for i in range(3):
        # check row
        if current_table[i][0] == current_table[i][1] == current_table[i][2] == player:

            return True
        # check column
        if current_table[0][i] == current_table[1][i] == current_table[2][i] == player:
            return True

        # main diagonal
        if current_table[0][0] == current_table[1][1] == current_table[2][2] == player:
            return True

        # second diagonal
        if current_table[0][2] == current_table[1][1] == current_table[2][0] == player:
            return True
    return False


def make_move(player, number, current_table):
    x, y = get_3x3_pos(number)
    new_state = copy.deepcopy(current_table)
    new_state[x][y] = player
    return new_state


def validate_move(player, number):
    x, y = get_3x3_pos(number)
    if TABLE[x][y] == 0:
        return True
    return False


def count_empty_directions(current_table):
    empty_directions = 0
    # check for empty rows
    for i in range(3):
        if current_table[i][0] == current_table[i][1] == current_table[i][2] == 0:
            empty_directions += 1
        if current_table[0][i] == current_table[1][i] == current_table[2][i] == 0:
            empty_directions += 1
    if current_table[0][0] == current_table[1][1] == current_table[2][2] == 0:
        empty_directions += 1
    if current_table[0][2] == current_table[1][1] == current_table[2][0] == 0:
        empty_directions += 1
    return empty_directions


def my_heuristic(current_table, player):
    max_value = -math.inf
    best_choice = 0
    print("Possible moves: ", choices)
    # for each possible move
    for choice in choices:
        # check how many directions are open for me and for the opponent
        open_for_me = count_empty_directions(current_table)

        temp_table = make_move(player, choice, current_table)

        open_for_opponent = count_empty_directions(temp_table)
        print(open_for_opponent, "open for opponent")
        if open_for_me - open_for_opponent > max_value:
            max_value = open_for_me - open_for_opponent
            best_choice = choice

    return best_choice


def my_heuristic_minmax(current_table, player):
    max_value = -9999
    best_choice = 0
    # if verify_win("A", current_table):
    #     return 100, 0
    # elif verify_win("B", current_table):
    #     return -100, 0
    if player == "A" and verify_win("A", current_table):
        return 100, 0
    elif player == "B" and verify_win("B", current_table):
        return -100, 0

    # for each possible move
    for choice_here in choices:
        # check how many directions are open for me and for the opponent
        open_for_me = count_empty_directions(current_table)
        # print_table(current_table)
        #print(open_for_me, "open for me")
        temp_table = make_move(player, choice_here, current_table)

        open_for_opponent = count_empty_directions(temp_table)
        # print(open_for_opponent, "open for opponent")
        if open_for_me - open_for_opponent > max_value:
            max_value = open_for_me - open_for_opponent
            best_choice = choice_here
            print("max val",max_value)
    return max_value, best_choice
def print_table(table):
    for i in range(3):
        print(table[i])
    print()


def simple_game():
    global TABLE
    current_state = TABLE
    player = "A"
    while len(choices) > 0:
        for i in range(3):
            print(current_state[i])
        print()
        if player == "A":  # A players turn
            next_move = my_heuristic(current_state, player)
            new_state = make_move(player, next_move, current_state)
            if validate_move(player, next_move):
                current_state = new_state
                player = "B"
                choices.remove(next_move)

            # for i in range(3):
            #     print(current_state[i])
            # print()
            # print("Possible moves: ", choices)
            # next_move = input("A's turn: ")
            # next_move = int(next_move)
            # new_state = make_move(player, next_move, current_state)
            # if validate_move(player, next_move):
            #     current_state = new_state
            #     player = "B"
            #     choices.remove(next_move)


        else:
            next_move = my_heuristic(current_state, player)

            new_state = make_move(player, next_move, current_state)
            if validate_move(player, next_move):
                current_state = new_state
                player = "A"
                choices.remove(next_move)

        if verify_win(player, current_state):
            print("Player ", player, " has won!")
            break

    return current_state


def game_with_minimax():
    global TABLE
    current_state = TABLE
    player = "A"
    win = False
    while len(choices) > 0:

        for i in range(3):
            print(current_state[i])
        print()

        if player == "A":  # A players turn
            # next_move = my_heuristic(current_state, player)
            # new_state = make_move(player, next_move, current_state)
            # if validate_move(player, next_move):
            #     current_state = new_state
            #     player = "B"
            #     choices.remove(next_move)
            print("Possible moves: ", choices)
            print()
            move = input("A's turn: ")
            move = int(move)
            new_state = make_move(player, move, current_state)
            if validate_move(player, move):
                current_state = new_state
                if verify_win(player, current_state):
                    print("Player ", player, " has won!")
                    win = True
                    break
                player = "B"
                choices.remove(move)

        else:
            best_move = None
            best_score = -9999
            for mutare in choices:
                choices_copy = copy.deepcopy(choices)
                choices_copy.remove(mutare)
                new_move = minimax(make_move(player, mutare, current_state), True, 4, choices_copy)
                print("best new score", new_move[0], "for move", mutare)
                if new_move[0] > best_score:
                    best_score = new_move[0]
                    best_move = mutare


            # next_move = minimax(current_state, True, 10, choices)[1]
            new_state = make_move(player, best_move, current_state)
            if validate_move(player, best_move):
                current_state = new_state
                if verify_win(player, current_state):
                    print("Player ", player, " has won!")
                    win = True
                    break
                player = "A"
                choices.remove(best_move)

    if not win:
        print("Draw!")

    return current_state


def check_draw(current_table):
    for i in range(3):
        for j in range(3):
            if current_table[i][j] == 0:
                return False
    return True


def minimax(current_table, is_max_player, depth, current_choices):
    # base case
    global choice
    current_table_copy = copy.deepcopy(current_table)
    if depth == 0 or verify_win("A", current_table):

        return my_heuristic_minmax(current_table_copy, "A")

    elif depth == 0 or verify_win("B", current_table):

        return my_heuristic_minmax(current_table_copy, "B")

    # elif depth == 0:
    #     return my_heuristic_minmax2(current_table, "B",is_max_player)
    elif check_draw(current_table):
        return 0, 0

    if is_max_player:
        value = -9999
        for choice in current_choices:
            new_choices = copy.deepcopy(current_choices)
            new_choices.remove(choice)
            current_table_copy = copy.deepcopy(current_table)
            minimax_result = minimax(make_move("B", choice, current_table_copy), False, depth - 1, new_choices)
            value = max(value, minimax_result[0])
            # print("maximizing", value, choice)
            # print(minimax_result,"result")
    else:
        value = math.inf
        for choice in current_choices:
            new_choices = copy.deepcopy(current_choices)
            new_choices.remove(choice)
            current_table_copy = copy.deepcopy(current_table)
            minimax_result = minimax(make_move("A", choice, current_table_copy), True, depth - 1, new_choices)
            # print(minimax_result,"result")
            value = min(value, minimax_result[0])
            # print("minimizing", value, choice)
    # print("value in minimax", value, choice)
    return value, choice


final_board = game_with_minimax()

for i in range(3):
    print(final_board[i])
