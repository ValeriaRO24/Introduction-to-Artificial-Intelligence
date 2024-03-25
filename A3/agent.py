"""
An AI player for Mancala.
"""

# Some potentially helpful libraries
import random
import math
import time

# You can use the functions in mancala_game to write your AI. Import methods you need.
from mancala_game import Board, get_possible_moves, eprint, play_move, MCTS

cache={} # Use this variable for your state cache; Use it if caching is on

# Implement the below functions. You are allowed to define additional functions that you believe will come in handy.
def compute_utility(board, side):
    # IMPLEMENT!
    """
    Method to compute the utility value of board. This is equal to the number of stones of the mancala
    of a given player, minus the number of stones in the opposing player's mancala.
    INPUT: a game state, the player that is in control
    OUTPUT: an integer that represents utility
    """


    if side == 0:
        return board.mancalas[0] - board.mancalas[1]
    else:
        return board.mancalas[1] - board.mancalas[0]

def compute_heuristic(board, color):
    # IMPLEMENT!
    """
    Method to compute the heuristic value of a specific state of the board.
    INPUT: a game state, the player that is in control, the depth limit for the search
    OUTPUT: an integer that represents heuristic value
    """

    """
    For my new heuristic I followed the same use of compute utility and added the heuristic 
    suggestions from the assignment outline. Where it keeps  track of how many empty pockets are in the
    given side, as well as the current score. 
    """
    curr_val = compute_utility(board, color)
    if helper_terminal(board):
        return curr_val

    for pocket in board.pockets[color]:
        if pocket == 0:
            curr_val += 1

    return curr_val + board.mancalas[color]

################### MINIMAX METHODS ####################
def select_move_minimax(board, color, limit=-1, caching = False):
    # IMPLEMENT!
    """
    Given a board and a player color, decide on a move using the MINIMAX ALGORITHM. The return value is
    an integer i, where i is the pocket that the player on side 'color' should select.
    INPUT: a game state, the player that is in control, the depth limit for the search, and a boolean that determines whether state caching is on or not
    OUTPUT: an integer that represents a move

    """

    '''
    if limit != 0:
        if helper_terminal(board):
            return compute_utility(board, color) #Return terminal states utility    //(U is specified as part of game)
        # #Apply Player’s moves to get successor states.

        ChildList = get_possible_moves(board, color) #n
        minval = math.inf
        maxval = -math.inf

        if color == 0:
            #for c in ChildList:
            minval = min([select_move_minimax(play_move(board, color, c),1, limit-1) for c in ChildList])#min(select_move_minimax(play_move(board, color, c), 1, limit-1, caching = False), minval)
                # instead try min([select_move_minimax(play_move(board, color, c), 1, limit-1, caching = False), for(c in childlist)])
                #x = [1, 2, 3, 4, 5]
                # >>> y = [2*a for a in x if a % 2 == 1]
                # [select_move_minimax(play_move(board, color, c) for c in ChildList]
            return minval
        else:
            #for c in ChildList:
            if len([select_move_minimax(play_move(board, color, c),0, limit-1) for c in ChildList]) == 0:
                return 0
            maxval = max([select_move_minimax(play_move(board, color, c),0, limit-1) for c in ChildList]) #max(select_move_minimax(play_move(board, color, c), 0, limit-1,  caching = False), maxval)
            return maxval
    else:
        return compute_utility(board, color)
    '''
    global cache
    cache = {}
    if limit % 2 == 0:
        return max_rec_helper(board, color, limit, caching)[1]
    else:
        return min_rec_helper(board, color, limit, caching)[1]


def min_rec_helper(board, color, limit, caching):
    global cache
    if helper_terminal(board):
        return compute_utility(board, color), None

    #if helper_terminal(board):
    # return compute_utility(board, color), None

    child_list = get_possible_moves(board, color)
    if limit != 0:
        min_val = math.inf
        min_child = None
        util = None
        played_board = None
        for c in child_list:

            played_board = play_move(board, color, c)
            if caching and played_board in cache and cache[played_board][0]:
                util = cache[played_board][1]
            else:
                if color == 0:
                    util = max_rec_helper(played_board, 1, limit -1, caching)[0]

                else:
                    util = max_rec_helper(played_board, 0, limit -1, caching)[0]

                if caching:
                    cache[played_board] = (True, util)
            if util < min_val:
                min_val  = util
                min_child = c
        return min_val, min_child
    return compute_utility(board, color), None


def max_rec_helper(board, color, limit, caching):
    global cache
    if helper_terminal(board):
        return compute_utility(board, color), None

    child_list = get_possible_moves(board, color)
    if limit != 0:
        max_val = -math.inf
        max_child = None
        util = None
        played_board = None
        for c in child_list:

            played_board = play_move(board, color, c)
            if caching and played_board in cache and cache[played_board][0]:
                util = cache[played_board][1]
            else:
                if color == 0:
                    util = min_rec_helper(played_board, 1, limit -1, caching)[0]

                else:
                    util = min_rec_helper(played_board, 0, limit -1, caching)[0]

                if caching:
                    cache[played_board] = (False, util)
            if util > max_val:
                max_val = util
                max_child = c
        return max_val, max_child


    return compute_utility(board, color), None


def helper_terminal(board):
    for i in board.pockets:
        if i == 0:
            return True
    return False
    ################### ALPHA-BETA METHODS ####################
def select_move_alphabeta(board, color, limit=-1, caching = False):
    # IMPLEMENT!
    """
    Given a board and a player color, decide on a move using the ALPHABETA ALGORITHM. The return value is
    an integer i, where i is the pocket that the player on side 'color' should select.
    INPUT: a game state, the player that is in control, the depth limit for the search, and a boolean that determines if state caching is on or not
    OUTPUT: an integer that represents a move
    """
    global cache
    cache = {}
    if limit % 2 == 0:
        return max_alphabeta_helper(board, color, limit, -math.inf, math.inf, caching)[1]
    else:
        return min_alphabeta_helper(board, color, limit, -math.inf, math.inf, caching)[1]


def min_alphabeta_helper(board, color, limit, alph, beta, caching):
    global cache

    if helper_terminal(board):
        return compute_utility(board, color), None

    if limit != 0:

        child_list = get_possible_moves(board, color)
        min_val = math.inf
        min_child = None
        util = None
        played_board = None


        for c in child_list:
            played_board = play_move(board, color, c)
            if caching and played_board in cache and cache[played_board][0]:
                util = cache[played_board][1]

            else:
                if color == 0:
                    util = max_alphabeta_helper(played_board, 1, limit -1, alph, beta, caching)[0]

                else:
                    util = max_alphabeta_helper(played_board, 0, limit -1, alph, beta, caching)[0]

                if caching:
                    cache[played_board] = (True, util)

            if util < min_val:
                min_val = util
                min_child = c
            if beta > min_val:
                beta = min_val
                if beta <= alph:

                    break



        return min_val, min_child

    return compute_utility(board, color), None


def max_alphabeta_helper(board, color, limit, alph, beta, caching):
    global cache

    if helper_terminal(board):
        return compute_utility(board, color), None

    if limit != 0:

        child_list = get_possible_moves(board, color)
        max_val = -math.inf
        max_child = None
        util = None
        played_board = None


        for c in child_list:
            played_board = play_move(board, color, c)
            if caching and played_board in cache and cache[played_board][0]:
                util = cache[played_board][1]

            else:
                if color == 0:
                    util = min_alphabeta_helper(played_board, 1, limit -1, alph, beta, caching)[0]

                else:
                    util = min_alphabeta_helper(played_board, 0, limit -1, alph, beta, caching)[0]

                if caching:
                    cache[played_board] = (False, util)

            if util > max_val:
                max_val = util
                max_child = c
            if alph < max_val:
                alph = max_val
                if beta <= alph:
                    break



        return max_val, max_child

    return compute_utility(board, color), None

################### MCTS METHODS ####################
def ucb_select(board, mcts_tree):
    # IMPLEMENT! This is the only function of MCTS that will be marked as a part of the assignment. Feel free to implement the others, but only if you like.
    """
    Given a board and its MCTS tree, select and return the successive state with the highest UCB
    INPUT: a board state and an MCTS tree
    OUTPUT: the successive state of the input board that corresponds with the max UCB value in the tree.
    """
    # Hint: You can encode this as follows:
    # 1. Cycle thru the successors of the given board.
    # 2. Calculate the UCB values for the successors, given the input tree
    # 3. Return the successor with the highest UCB value
    ''' 
    
    children1 = get_possible_moves(board, 1)
    new_boards = []

    for c in children1:
        new_boards.append(play_move(board, 1, c))



    children0 = get_possible_moves(board, 0)
    '''
    #new_board = play_move(board, 1, get_possible_moves(board, 1)[0])
    children1 = get_possible_moves(board, 0)
    new_boards = []

    for c in children1:
        new_boards.append(play_move(board, 0, c))

    children2 = get_possible_moves(board, 1)

    for c in children2:
        new_boards.append(play_move(board, 1, c))

    #these are the successors to check

    #now for each check the UCB, use the monte carlo to get the amount of times visted etc but first
    #check if in the director
    highest_UCB = 0
    successor = None
    c = mcts_tree.weight
    N = 0
    move = 0
    #counts of parent
    if board in mcts_tree.counts:

        N = math.log(mcts_tree.counts[board])


    for succ in mcts_tree.successors[board]:
        #calculate UCB
        new_ucb = 0
        succ2 = succ[0]
        vi = 0 #Estimated value of the node
        ni = 1 #number of times the node has been visited

        check = True
        if succ2 in mcts_tree.counts:
            ni = mcts_tree.counts[succ2]
        else:
            check = False
        if succ2 in mcts_tree.rewards:
            vi = mcts_tree.rewards[succ2] / mcts_tree.counts[succ2]

        else:
            check = False

        new_ucb = math.floor(vi + (c * (math.sqrt(N/ni))))

        if new_ucb > highest_UCB and check:
            highest_UCB = new_ucb
            successor = succ2
            move = succ[1]

    def uct(succ):
        succ = succ[0]
        return math.floor(mcts_tree.rewards[succ] / mcts_tree.counts[succ]
                          + (mcts_tree.weight * (math.sqrt(math.log(mcts_tree.counts[board])/mcts_tree.counts[succ]))))

    return max(mcts_tree.successors[board], key=uct)



#######################################################################
#######################################################################
####### IMPLEMENTATION OF ALL MCTS METHODS BELOW IS OPTIONAL ###############
#######################################################################
#######################################################################

def choose_move(board, color, mcts_tree):
    # IMPLEMENT! (OPTIONAL)
    '''choose a move'''
    '''INPUT: a game state, the player that is in control and an MCTS tree'''
    '''OUTPUT: a number representing a move for the player tat is in control'''
    # Encoding this method is OPTIONAL.  You will want it to
    # 1. See if a given game state is in the MCTS tree.
    # 2. If yes, return the move that is associated with the highest average reward in the tree (from the perspective of the player 'color')
    # 3. If no, return a random move
    raise RuntimeError("Method not implemented") # Replace this line!


def rollout(board, color, mcts_tree):
    # IMPLEMENT! (OPTIONAL)
    '''rollout the tree!'''
    '''INPUT: a game state that will be at the start of the path, the player that is in control and an MCTS tree (see class def in mancala_game)'''
    '''OUTPUT: nothing!  Just adjust the MCTS tree statistics as you roll out.'''
    # You will want it to:
    # 1. Find a path from the root of the tree to a leaf based on ucs stats (use select_path(board, color, mctsree))
    # 2. Expand the last state in that path and add all the successors to the tree (use expand_leaf(board, color, mctsree))
    # 3. Simulate game play from the final state to a terminal and derive the reward
    # 4. Back-propagate the reward all the way from the terminal to the root of the MCTS tree
    raise RuntimeError("Method not implemented") # Replace this line!


def select_path(board, color, mcts_tree):
    # IMPLEMENT! (OPTIONAL)
    '''Find a path from the root of the tree to a leaf based on ucs stats'''
    '''INPUT: a game state that will be at the start of the path, the player that is in control and an MCTS tree (see class def in mancala_game)'''
    '''OUTPUT: A list of states that leads from the root of the MCTS tree to a leaf.'''
    # You will want it to return a path from the board provided to a
    # leaf of the MCTS tree based on ucs stats (select_path(board, mctsree)). You can encode this as follows:
    # Repeat:
    # 1. Add the state to the path
    # 2. Check to see if the state is a terminal.  If yes, return the path.
    # 3. If no, check to see if any successor of the state is a terminal.  If yes, add any unexplored terminal to the path and return.
    # 5. If no, descend the MCTS tree a level to select a new state based on the UCT criteria.
    raise RuntimeError("Method not implemented") # Replace this line!

def expand_leaf(board, color, mcts_tree):
    # IMPLEMENT! (OPTIONAL)
    '''Expand a leaf in the mcts tree'''
    '''INPUT: a game state that will be at the start of the path, the player that is in control and an MCTS tree (see class def in mancala_game)'''
    '''OUTPUT: nothing!  Just adjust the MCTS tree statistics as you roll out.'''
    # If the given state already exists in the tree, do nothing
    # Else, add the successors of the state to the tree.
    raise RuntimeError("Method not implemented") # Replace this line!


def simulate(board, color):
    # IMPLEMENT! (OPTIONAL)
    '''simulate game play from a state to a leaf'''
    '''INPUT: a game state, the player that is in control'''
    '''OUTPUT: a reward that the controller of the tree can hope to get from this state!'''
    # You can encode this as follows:
    # 1. Get all the possible moves from the state. If there are none, return the reward that the player in control can expect to get from the state.
    # 2. Select a moves at random, and play it to generate a new state
    # 3. Repeat.
    # Remember:
    #  -- the reward the controlling player receives at one level will be the OPPOSITE of the reward at the next level!
    #  -- at one level the player in control will play a move, and at the next his or her opponent will play a move!
    raise RuntimeError("Method not implemented") # Replace this line!

def backprop(path, reward, mcts_tree):
    # IMPLEMENT! (OPTIONAL)
    '''backpropagate rewards a leaf to the root of the tree'''
    '''INPUT: the path leading from a state to a terminal, the reward to propagate, and an MCTS tree'''
    '''OUTPUT: nothing!  Just adjust the MCTS tree statistics as you roll out.'''
    # You can encode this as follows:
    # FROM THE BACK TO THE FRONT OF THE PATH:
    # 1. Update the number of times you've seen a given state in the MCTS tree
    # 2. Update the reward associated with that state in the MCTS tree
    # 3. Continue
    # Remember:
    #  -- the reward one level will be the OPPOSITE of the reward at the next level!  Make sure to update the rewards accordingly
    raise RuntimeError("Method not implemented") # Replace this line!

def select_move_mcts(board, color, weight=1, numsamples = 50):
    # IMPLEMENT! (OPTIONAL)
    mcts_tree = MCTS(weight) # Initialize your MCTS tree
    for _ in range(numsamples): # Sample the tree numsamples times
        # In here you'll want to encode a 'rollout' for each iteration
        # store the results of each rollout in the MCTS tree (mcts_tree)
        pass # Replace this line!

    # Then, at the end of your iterations, choose the best move, according to your tree (ie choose_move(board, color, mcts_tree))
    raise RuntimeError("Method not implemented") # Replace this line!

#######################################################################
#######################################################################
################### END OF OPTIONAL FUNCTIONS #########################
#######################################################################
#######################################################################

def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Mancala AI")  # First line is the name of this AI
    arguments = input().split(",")

    color = int(arguments[0])  # Player color
    limit = int(arguments[1])  # Depth limit
    CACHING = int(arguments[2]) # caching or no?
    algorithm = int(arguments[3])  # Minimax, Alpha Beta, or MCTS

    if (algorithm == 2): # Implement this only if you really want to!!
        eprint("Running MCTS")
        limit = -1  # Limit is irrelevant to MCTS!!
    elif (algorithm == 1):
        eprint("Running ALPHA-BETA")
    else:
        eprint("Running MINIMAX")

    if (CACHING == 1):
        eprint("Caching is ON")
    else:
        eprint("Caching is OFF")

    if (limit == -1):
        eprint("Depth Limit is OFF")
    else:
        eprint("Depth Limit is ", limit)

    while True:  # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()

        if status == "FINAL":  # Game is over.
            print
        else:
            pockets = eval(input())  # Read in the pockets on the board
            mancalas = eval(input())  # Read in the mancalas on the board
            board = Board(pockets, mancalas) #turn info into an object

            # Select the move and send it to the manager
            if (algorithm == 2):
                move = select_move_mcts(board, color, numsamples=50) #50 samples per iteration by default
            elif (algorithm == 1):
                move = select_move_alphabeta(board, color, limit, bool(CACHING))
            else:
                move = select_move_minimax(board, color, limit, bool(CACHING))

            print("{}".format(move))


if __name__ == "__main__":
    run_ai()
