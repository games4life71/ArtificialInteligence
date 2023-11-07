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


def count_empty_directions(current_table: list):
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
    # for each possible move
    for choice in choices:
        # check how many directions are open for me and for the opponent
        open_for_me = count_empty_directions(current_table)

        temp_table = make_move(player, choice, current_table)

        open_for_opponent = count_empty_directions(temp_table)

        if open_for_me - open_for_opponent > max_value:
            max_value = open_for_me - open_for_opponent
            best_choice = choice

    return best_choice


def my_heuristic_minmax(current_table, player):
    max_value = -math.inf
    best_choice = 0
    # for each possible move
    for choice in choices:
        # check how many directions are open for me and for the opponent
        open_for_me = count_empty_directions(current_table)

        temp_table = make_move(player, choice, current_table)

        open_for_opponent = count_empty_directions(temp_table)

        if open_for_me - open_for_opponent > max_value:
            max_value = open_for_me - open_for_opponent
            best_choice = choice

    return max_value, best_choice


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
            next_move = minimax(current_state, True, 200, choices)[1]
            new_state = make_move(player, next_move, current_state)
            if validate_move(player, next_move):
                current_state = new_state
                if verify_win(player, current_state):
                    print("Player ", player, " has won!")
                    win = True
                    break
                player = "A"
                choices.remove(next_move)

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
    if depth == 0 or verify_win("A", current_table):
        return my_heuristic_minmax(current_table, "A")

    elif depth == 0 or verify_win("B", current_table):
        return my_heuristic_minmax(current_table, "B")
    elif check_draw(current_table):
        return 0, 0

    if is_max_player:
        value = -math.inf
        for choice in current_choices:
            new_choices = copy.deepcopy(current_choices)
            new_choices.remove(choice)
            minimax_result = minimax(make_move("B", choice, current_table), False, depth - 1, new_choices)
            value = max(value, minimax_result[0])
            # print(minimax_result,"result")
    else:
        value = math.inf
        for choice in current_choices:
            new_choices = copy.deepcopy(current_choices)
            new_choices.remove(choice)
            minimax_result = minimax(make_move("A", choice, current_table), True, depth - 1, new_choices)
            # print(minimax_result,"result")
            value = min(value, minimax_result[0])

    return value, choice


final_board = game_with_minimax()
for i in range(3):
    print(final_board[i])
