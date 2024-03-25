#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the Rush Hour domain.

#   You may add only standard python imports (numpy, itertools are both ok).
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files.

import os  # you will likely want this for timing functions
import math # for infinity
from search import *  # for search engines
from rushhour import *

# RUSH HOUR GOAL TEST
def rushhour_goal_fn(state):
    # IMPLEMENT
    '''a Rush Hour Goal Test'''
    '''INPUT: a parking state'''
    '''OUTPUT: True, if satisfies the goal, else false.'''

    cars = state.get_vehicle_statuses()
    board = state.get_board_properties()

    #print(board[2])
    #board[1] == entrance
    #board[2] == direction

    for car in cars:
        if car[4]: #if car is goal car


            if board[2] == 'N' and car[1] == board[1] and not car[3]:
                return True
            if board[2] == 'S' and car[1][0] == board[1][0] and not car[3]:
                sizeloc = car[1][1] + (car[2] - 1)

                if sizeloc >= board[0][0]:
                    sizeloc -= board[0][0]

                if sizeloc == board[1][1]:
                    return True

            if board[2] == "W" and car[1] == board[1] and car[3]:
                return True

            if board[2] == "E" and car[1][1] == board[1][1] and car[3]:
                sizeloc2 = car[1][0] + (car[2] - 1)

                if sizeloc2 >= board[0][1]:
                    sizeloc2 -= board[0][1]

                if sizeloc2 == board[1][0]:
                    return True

    return False





# RUSH HOUR HEURISTICS
def heur_alternate(state):
    # IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a tokyo parking state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''

    #HEURISTIC EXPLINATION:
    #For this improved heuristic I've taken the properties of min_dist function and improved it
    #by also looking at the cars that get in the way of the goal cars and the entrance of the goal
    #so now it not only tracks the min_distance of a goal car from the entrance, but also sees
    #how many cars are in the same path of the goal entrance by comparing the locations of the non-
    #goal cars to the location of the entrance, wether it is N S or W E, so that in the way will add to
    #the hueristic because this would increase the path from a goal_car to the entrance.

    #For my alternate heuristic I had a difficult time adding more strategies to build a heuristic when
    #time is a big factor, as I did not want to add more programming code that would increase the
    #run time.

    #First getting the board and vehicle properties of the state
    cars = state.get_vehicle_statuses()
    board = state.get_board_properties()
    #board[1] == entrance
    #board[2] == direction

    in_way_car = 1
    min_value = math.inf

    #Start by iterating through every vehicle in board
    for car in cars:
        #This if statement is to check if the vehicle is not a goal car, if so, it checks its location
        #in constrast with the entrance, and adds to the heuristic if there is a chance for it to be
        #blocking the way for a goal_car to reach the entrance
        if not car[4]:
            if (board[2] == 'N' or board[2] == 'S') and car[1][0] == board[1][0]:
                in_way_car += 1

            if (board[2] == 'W' or board[2] == 'E') and car[1][1] == board[1][1]:
                in_way_car += 1

        #Now it check if a vehicle is a goal car, the further if statements are broken down into
        #two subcatagories, horizontal and vertical, which decreases the amount of if statements to use
        #we only care if the goal car is aligned, since it has to fit with the entrance
        if car[4]:

            if car[3] : #checks for horizontal
                count1 = car[1][0]
                #We want to check sizes of cars so that we know which cars will touch the entrance fastests
                if (car[1][0] + (car[2] - 1)) < board[0][0]: #this will give us the east most end of the vehicle
                    count2 = car[1][0] + (car[2] - 1)
                else: #Here we know the vehicle will wrap around the board
                    count2 = car[1][0] + board[0][1] - board[1][0]

                #Calculate the possible distance with a horizontal vehicle, (the west end of the vehicle to the entrance and vice versa)
                dist1 = min(abs(board[1][0] - count1), abs(board[1][0] - count2))
                dist2 = min(abs(board[0][1] + count1 - board[1][0]), abs(board[0][1] + count2 - board[1][0]))

                #Find the minimum distance as to know which vehicle is best
                if min(dist1, dist2) < min_value:
                    min_value = min(dist1, dist2)

            #checks for not horizontal (Vertical)
            if not car[3] : #and (car[1][0] == board[1][0])
                count1 = car[1][1]

                if (car[1][1] + (car[2] - 1)) < board[0][1]: #this will give us the south most end of the vehicle
                    count2 = car[1][1] + (car[2] - 1)
                else: #Wraps around board
                    count2 = car[1][1] + (car[2] - 1) - board[0][1]

                #Calculate the possible distance with a vertical vehicle, (the south end of the vehicle to the entrance and vice versa)
                dist1 = min(abs(board[1][1] - count1), abs(board[1][1] - count2))
                dist2 = min(abs(board[0][0] - count1 + board[1][1]), abs(board[0][0] - count2 + board[1][1]))

                #Find the minimum distance as to know which vehicle is best
                if min(dist1, dist2) < min_value:
                    min_value = min(dist1, dist2)
#Now we put the algorithms together to generate the heuristic
    return min_value + in_way_car



    ''' 
    for car in cars:
        #there are four cases depending on direction of the entrance
        if car[4] and board[2] == 'N' and not car[3]:
            count = abs(board[1][1] - car[1][1])
            if count < min_value:
                min_value = count

            #continue

        if car[4] and board[2] == 'S'and not car[3]:
            sizeloc = car[1][1] + (car[2] - 1)
            if sizeloc >= board[0][0]:
                sizeloc -= board[0][0]

            count = abs(board[1][1] - sizeloc)
            if count < min_value:
                min_value = count
            #continue

        if car[4] and board[2] == 'W' and car[3]:
            count = abs(board[1][0] - car[1][0])
            if count < min_value:
                min_value = count
            #continue

        if car[4] and board[2] == 'E' and car[3]:
            sizeloc = car[1][0] + (car[2] - 1)
            if sizeloc >= board[0][1]:
                sizeloc -= board[0][1]

            count = abs(board[1][1] - sizeloc)
            if count < min_value:
                min_value = count
            #continue
    
    
    
    
    
    if not min_car[4]:
        print("in here -99")
        return -99
        
    for car in cars:
        if not car[4] and car[3]:
            #car that is horizontal
            if car[]
            
            min_value = heur_min_dist(state)
            min_value + 1

    '''


def heur_min_dist(state):
    #IMPLEMENT
    '''admissible tokyo parking puzzle heuristic'''
    '''INPUT: a tokyo parking state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # We want an admissible heuristic, which is an optimistic heuristic.
    # It must never overestimate the cost to get from the current state to the goal.
    # Getting to the goal requires one move for each tile of distance.
    # Since the board wraps around, there will be two different directions that lead to a goal.
    # NOTE that we want an estimate of the number of moves required from our current state
    # 1. Proceeding in the first direction, let MOVES1 =
    #    number of moves required to get to the goal if it were unobstructed and if we ignore the orientation of the goal
    # 2. Proceeding in the second direction, let MOVES2 =
    #    number of moves required to get to the goal if it were unobstructed and if we ignore the orientation of the goal
    #
    # Our heuristic value is the minimum of MOVES1 and MOVES2 over all goal vehicles.
    # You should implement this heuristic function exactly, and you can improve upon it in your heur_alternate

    cars = state.get_vehicle_statuses()
    board = state.get_board_properties()
    #board[1] == entrance
    #board[2] == direction

    count = 0
    goal_cars = []
    #min_value = 1000000000 #Let's start with a value way higher than any possible (change later if found better way)
    min_value = math.inf #better alternative
    for car in cars:
        if car[4]:
            goal_cars.append(car)

    for car in goal_cars:

        if car[3] and (car[1][1] == board[1][1]):
            #count1 = abs(board[1][0] - car[1][0])
            count1 = car[1][0]

            if (car[1][0] + (car[2] - 1)) < board[0][0]:
                count2 = car[1][0] + (car[2] - 1)
            else:
                count2 = car[1][0] + board[0][1] - board[1][0]

            dist1 = min(abs(board[1][0] - count1), abs(board[1][0] - count2))
            dist2 = min(abs(board[0][1] + count1 - board[1][0]), abs(board[0][1] + count2 - board[1][0]))

            #min_value = min(dist1, dist2)
            if min(dist1, dist2) < min_value:
                min_value = min(dist1, dist2)

            #sizeloc = car[1][0] + (car[2] - 1)
            #if sizeloc >= board[0][1]:
            #    sizeloc -= board[0][1]

            #count2 = abs(board[1][0] - sizeloc)
            #if min(count1, count2) < min_value:
                #min_value = min(count1, count2)

        if not car[3] and (car[1][0] == board[1][0]):
            count1 = car[1][1]

            if (car[1][1] + (car[2] - 1)) < board[0][1]:
                count2 = car[1][1] + (car[2] - 1)
            else:
                count2 = car[1][1] + (car[2] - 1) - board[0][1]

            dist1 = min(abs(board[1][1] - count1), abs(board[1][1] - count2))
            dist2 = min(abs(board[0][0] - count1 + board[1][1]), abs(board[0][0] - count2 + board[1][1]))

            if min(dist1, dist2) < min_value:
                min_value = min(dist1, dist2)

            #sizeloc = car[1][1] + (car[2] - 1)
            #if sizeloc >= board[0][0]:
                #sizeloc -= board[0][0]
            #count2 = abs(board[1][1] - sizeloc)

            #if min(count1, count2) < min_value:
                #min_value = min(count1, count2)

    return min_value



def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def fval_function(sN, weight):
    # IMPLEMENT
    """
    Provide a custom formula for f-value computation for Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Weighted A star
    @rtype: float
    """
    # g(n) is the sN.gval
    #f(n) = g(n) + H*h(n)

    return sN.gval + (weight * sN.hval)

def fval_function_XUP(sN, weight):
    #IMPLEMENT
    """
    Another custom formula for f-value computation for Weighted A star.
    Returns the fval of the state contained in the sNode.
    XUP causes the best-first search to explore near-optimal paths near the end of a path.

    @param sNode sN: A search node (containing a RushHour State)
    @param float weight: Weight given by Weighted A star
    @rtype: float
    """
    #(1/2w)(g(node) + h(node) + sqrt((g(node)+h(node))2+4w(w-1)h(node)2))

    return (1/(2*weight)) * (sN.gval + sN.hval + math.sqrt((sN.gval + sN.hval)**2 + 4*weight*(weight-1) * (sN.hval)**2))


def fval_function_XDP(sN, weight):
    #IMPLEMENT
    """
    A third custom formula for f-value computation for Weighted A star.
    Returns the fval of the state contained in the sNode.
    XDP causes the best-first search to explore near-optimal paths near the start of a path.

    @param sNode sN: A search node (containing a RushHour State)
    @param float weight: Weight given by Weighted A star
    @rtype: float
    """
    #(1/2w)[g(node)+(2w-1)h(node)+sqrt((g(node)-h(node))^2+4wg(node)h(node))]
    return (1/(2*weight)) * (sN.gval + (2*weight - 1)*sN.hval + math.sqrt((sN.gval - sN.hval)**2 + 4*weight * (sN.hval) * (sN.gval)))

# SEARCH ALGORITHMS
def weighted_astar(initial_state, heur_fn, weight, timebound, costbound = (float(math.inf), float(math.inf), float(math.inf))):
    # IMPLEMENT
    """
    Provides an implementation of weighted a-star, as described in the HW1 handout'''
    INPUT: a rushhour state that represents the start state and a timebound (number of seconds)
    OUTPUT: A goal state (if a goal is found), else False as well as a SearchStats object
    implementation of weighted astar algorithm

    @param initial_state: A RushHour State
    @param heur_fn: The heuristic to use
    @param weight: The weight to use
    @param timebound: The timebound to enforce
    @param costbound: The costbound to enforce, if any
    @rtype: (Rushour State, SearchStats) if solution is found, else (False, SearchStats)
    """
    search = SearchEngine(strategy='custom')
    search.init_search(initial_state, (lambda state: rushhour_goal_fn(state)), heur_fn, (lambda sN: fval_function(sN, weight)))
    return search.search(timebound=timebound, costbound=costbound)


def iterative_astar(initial_state, heur_fn, weight=1, timebound=5):  # uses f(n), see how autograder initializes a search
    # IMPLEMENT
    """
    Provides an implementation of iterative a-star, as described in the HW1 handout
    INPUT: a rushhour state that represents the start state and a timebound (number of seconds)
    OUTPUT: A goal state (if a goal is found), else False as well as a SearchStats object
    implementation of weighted astar algorithm

    @param initial_state: A RushHour State
    @param heur_fn: The heuristic to use
    @param weight: The weight to begin with during the first iteration (this should change)
    @param timebound: The timebound to enforce
    @rtype: (Rushour State, SearchStats) if solution is found, else (False, SearchStats)
    """
    timer = os.times()[0]

    goal, astar_stat = weighted_astar(initial_state=initial_state, heur_fn=heur_fn, weight=weight, timebound=timebound)
    if goal:
        costbound = (float(math.inf), float(math.inf), goal.gval)
        return_goal, return_stat = goal, astar_stat

        timebound -= (os.times()[0] - timer)

        while timebound > 0:
            timer = os.times()[0]
            goal, astar_stat = weighted_astar(initial_state=initial_state, heur_fn=heur_fn, weight=weight, timebound=timebound, costbound=costbound)
            timebound -= (os.times()[0] - timer)

            if goal:
                costbound = (float(math.inf), float(math.inf), goal.gval)
                return_goal, return_stat = goal, astar_stat


        return return_goal, return_stat

    return False, None


def iterative_gbfs(initial_state, heur_fn, timebound=5):  # only use h(n)
    # IMPLEMENT
    """
    Provides an implementation of anytime greedy best-first search, as described in the HW1 handout
    INPUT: a rush hour state that represents the start state and a timebound (number of seconds)
    OUTPUT: A goal state (if a goal is found), else False

    @param initial_state: A RushHour State
    @param heur_fn: The heuristic to use
    @param timebound: The timebound to enforce
    @rtype: (Rushour State, SearchStats) if solution is found, else (False, SearchStats)
    """
    timer = os.times()[0]

    goal, astar_stat = weighted_astar(initial_state=initial_state, heur_fn=heur_fn, weight=0, timebound=timebound)

    if goal:
        costbound = (float(math.inf), float(math.inf), goal.gval)
        return_goal, return_stat = goal, astar_stat

        timebound -= (os.times()[0] - timer)

        while 0 < timebound:
            timer = os.times()[0]
            goal, astar_stat = weighted_astar(initial_state=initial_state, heur_fn=heur_fn, weight=0, timebound=timebound, costbound=costbound)
            timebound -= (os.times()[0] - timer)

            if goal:
                costbound = (float(math.inf), float(math.inf), goal.gval)
                return_goal, return_stat = goal, astar_stat


        return return_goal, return_stat

    return False, None

