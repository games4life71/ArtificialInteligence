#this is the model of a given state
class ModelState:
    #the state of the puzzle
    # state = None
    # lastMove = None
    def __init__(self,state, lastMove):
        self.state = state
        self.lastMove = lastMove

    #function that return the position of the 0 in the state
    def get_zero_pos(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return (i,j)


def print_state(state):
    for row in state:
        print(row)
    print('\n')

def check_legal_move(state:ModelState,move:str,moved_cell:tuple):
    #check if the move is legal for this state
    if move == 'up':
        if moved_cell[0] == 0:
            return False
    elif move == 'down':
        if moved_cell[0] == 2:
            return False
    elif move == 'left':
        if moved_cell[1] == 0:
            return False
    elif move == 'right':
        if moved_cell[1] == 2:
            return False
    #if the last move is the opposite of the current move, return false

    if state.lastMove is None:
        return True
    if state.lastMove == 'up' and move == 'down':
        return False
    elif state.lastMove == 'left' and move == 'right':
        return False

    return True

def transition_move(state:ModelState,move:str,moved_cell:tuple):
    #check for the legality of the move
    if not check_legal_move(state,move,moved_cell):
        #the move is illegal
        raise Exception('Illegal move')
    #swap the 0 with the cell according to the move
    new_state = state.state
    #swap the values of the cells
    if move == 'up':
        new_state[moved_cell[0]][moved_cell[1]] = new_state[moved_cell[0]-1][moved_cell[1]]
        new_state[moved_cell[0]-1][moved_cell[1]] = 0
    elif move == 'down':
        new_state[moved_cell[0]][moved_cell[1]] = new_state[moved_cell[0]+1][moved_cell[1]]
        new_state[moved_cell[0]+1][moved_cell[1]] = 0
    elif move == 'left':
        new_state[moved_cell[0]][moved_cell[1]] = new_state[moved_cell[0]][moved_cell[1]-1]
        new_state[moved_cell[0]][moved_cell[1]-1] = 0
    elif move == 'right':
        new_state[moved_cell[0]][moved_cell[1]] = new_state[moved_cell[0]][moved_cell[1]+1]
        new_state[moved_cell[0]][moved_cell[1]+1] = 0
    new_state = ModelState(new_state,move)
    return new_state

#a function that returns the possible moves for a given state
def possible_moves(state:ModelState):
    #get the position of the 0 in the state
    zero_pos = state.get_zero_pos()
    #get the possible moves
    possible_moves = []
    if check_legal_move(state,'up',zero_pos):
        possible_moves.append('up')
    if check_legal_move(state,'down',zero_pos):
        possible_moves.append('down')
    if check_legal_move(state,'left',zero_pos):
        possible_moves.append('left')
    if check_legal_move(state,'right',zero_pos):
        possible_moves.append('right')

    return possible_moves

def check_final_state(current_state:ModelState):
    #check if the state is the final state
    #transform the 2d array into a 1d array
    state = []
    for row in current_state.state:
        for cell in row:
            if cell != 0:
                state.append(cell)

    for number in range(0,7):  #1 2 4
        if  state[number+1]-1 != state[number]:
            return False
    return True

#define an initial state as a global variable


def transform_input(input_array :list ):
    #transform the input array into a 2d array
    state = []
    for i in range(0,3):
        row = []
        for j in range(0,3):
            row.append(input_array[i*3+j])
        state.append(row)
    return state


#implement IDDFS algorithm
def IDDFS(initialState:ModelState,max_depth):
    for depth  in (0,max_depth):
        visited = []
        sol = depth_limited_DFS(initialState,depth,visited)
        if sol is not None:
            return sol

    return None

def print_linear_state (state):
    for cell in state:
        print(cell,end=' ')
    print('\n')
def depth_limited_DFS(current_state:ModelState,depth,visited):
    #check if the current state is the final state
    if check_final_state(current_state):
        #print_state(new_state.state)
        return current_state

    #check if the depth is 0
    if depth == 0:
        return None

    #get the possible moves for the current state
    possible_moves_array = possible_moves(current_state)
    #for each possible move
    visited.append(current_state)

    for move in possible_moves_array :
        #get the position of the 0 in the current state
        zero_pos = current_state.get_zero_pos()
        #get the new state after the move
        new_state = transition_move(current_state,move,zero_pos)
        #print_state(new_state.state)
        #check if the new state was visited
        if new_state not in visited:
            #add the new state to the visited states
            visited.append(new_state)
            print_linear_state(new_state.state)
            #call the function recursively
            sol = depth_limited_DFS(new_state,depth-1,visited)
            if sol is not None:
                return sol
    return None


initialState = ModelState(transform_input([2, 7, 5, 0, 8, 4, 3, 1, 6]   ), None)
sol = IDDFS(initialState,15)
if sol is not None:
    print('Solution found ! ')
    print_state(sol.state)
#print(check_final_state(initialState))
#initialState = ModelState([[1,2,4],[3,0,5],[6,7,8]], None)

