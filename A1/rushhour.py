'''
Rushhour STATESPACE
'''
#   You should not need to alter this file. Some methods may help you with testing.
from search import *
from random import Random
from string import ascii_lowercase as names

##################################################
# The search space class 'Rushhour'             #
# This class is a sub-class of 'StateSpace'      #
##################################################
class Vehicle(object):
    def __init__(self, name, loc, length, is_horizontal, is_goal):
        self.name = name
        self.loc = loc
        self.length = length
        self.is_horizontal = is_horizontal
        self.is_goal = is_goal

    def copy_and_update_loc(self, loc):
        """Copy this vehicle."""
        copy_of_self = Vehicle(self.name, loc, self.length, self.is_horizontal, self.is_goal)
        return copy_of_self

class Rushhour(StateSpace):
    def __init__(self, action, gval, parent, board_properties, vehicle_list):
        """Initialize a rushhour search state object."""
        StateSpace.__init__(self=self, action=action, gval=gval, parent=parent)
        self.board_properties = board_properties
        self.vehicle_list = vehicle_list

    def successors(self):
        '''Return list of rushhour objects that are the successors of the current object'''
        def get_occupancy_grid(board_size, vehicle_statuses):
            (m, n) = board_size
            board = [list([False] * n) for i in range(m)]
            for vs in vehicle_statuses:
                for i in range(vs[2]):  # vehicle length
                    if vs[3]:
                        # vehicle is horizontal
                        board[vs[1][1]][(vs[1][0] + i) % n] = True
                    else:
                        # vehicle is vertical
                        board[(vs[1][1] + i) % m][vs[1][0]] = True
            return board

        def get_north_succs(occupancy_grid, vehicle_list, board_properties):
            board_size = board_properties[0]
            states = list()
            for vehicle in vehicle_list:
                if vehicle.is_horizontal or (vehicle.length != board_size[0] and occupancy_grid[(vehicle.loc[1] - 1) % board_size[0]][vehicle.loc[0]]):
                    continue
                else:
                    new_vehicle = vehicle.copy_and_update_loc((vehicle.loc[0], (vehicle.loc[1] - 1) % board_size[0]))
                    new_vehicle_list = list(vehicle_list)
                    new_vehicle_list.remove(vehicle)
                    new_vehicle_list.append(new_vehicle)
                    states.append(Rushhour(action='move_vehicle({}, N)'.format(vehicle.name),
                                           gval=self.gval + 1,
                                           parent=self,
                                           board_properties=board_properties,
                                           vehicle_list=new_vehicle_list))
            return states

        def get_south_succs(occupancy_grid, vehicle_list, board_properties):
            board_size = board_properties[0]
            states = list()
            for vehicle in vehicle_list:
                if vehicle.is_horizontal or (vehicle.length != board_size[0] and occupancy_grid[(vehicle.loc[1] + vehicle.length) % board_size[0]][vehicle.loc[0]]):
                    continue
                else:
                    new_vehicle = vehicle.copy_and_update_loc((vehicle.loc[0], (vehicle.loc[1] + 1) % board_size[0]))
                    new_vehicle_list = list(vehicle_list)
                    new_vehicle_list.remove(vehicle)
                    new_vehicle_list.append(new_vehicle)
                    states.append(Rushhour(action='move_vehicle({}, S)'.format(vehicle.name),
                                           gval=self.gval + 1,
                                           parent=self,
                                           board_properties=board_properties,
                                           vehicle_list=new_vehicle_list))
            return states

        def get_west_succs(occupancy_grid, vehicle_list, board_properties):
            board_size = board_properties[0]
            states = list()
            for vehicle in vehicle_list:
                if not vehicle.is_horizontal or (vehicle.length != board_size[1] and occupancy_grid[vehicle.loc[1]][(vehicle.loc[0] - 1) % board_size[1]]):
                    continue
                else:
                    new_vehicle = vehicle.copy_and_update_loc(((vehicle.loc[0] - 1) % board_size[1], vehicle.loc[1]))
                    new_vehicle_list = list(vehicle_list)
                    new_vehicle_list.remove(vehicle)
                    new_vehicle_list.append(new_vehicle)
                    states.append(Rushhour(action='move_vehicle({}, W)'.format(vehicle.name),
                                           gval=self.gval + 1,
                                           parent=self,
                                           board_properties=board_properties,
                                           vehicle_list=new_vehicle_list))
            return states

        def get_east_succs(occupancy_grid, vehicle_list, board_properties):
            board_size = board_properties[0]
            states = list()
            for vehicle in vehicle_list:
                if not vehicle.is_horizontal or (vehicle.length != board_size[1] and occupancy_grid[vehicle.loc[1]][(vehicle.loc[0] + vehicle.length) % board_size[1]]):
                    continue
                else:
                    new_vehicle = vehicle.copy_and_update_loc(((vehicle.loc[0] + 1) % board_size[1], vehicle.loc[1]))
                    new_vehicle_list = list(vehicle_list)
                    new_vehicle_list.remove(vehicle)
                    new_vehicle_list.append(new_vehicle)
                    states.append(Rushhour(action='move_vehicle({}, E)'.format(vehicle.name),
                                           gval=self.gval + 1,
                                           parent=self,
                                           board_properties=board_properties,
                                           vehicle_list=new_vehicle_list))
            return states

        occupancy_grid = get_occupancy_grid(self.board_properties[0], self.get_vehicle_statuses())
        return list(get_north_succs(occupancy_grid, self.vehicle_list, self.board_properties)
                + get_south_succs(occupancy_grid, self.vehicle_list, self.board_properties)
                + get_east_succs(occupancy_grid, self.vehicle_list, self.board_properties)
                + get_west_succs(occupancy_grid, self.vehicle_list, self.board_properties))

    def hashable_state(self): 
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent the state.'''
        return tuple(sorted([tuple(status) for status in self.get_vehicle_statuses()]))

    def print_state(self):
        # DO NOT CHANGE THIS FUNCTION
        # Print an ASCII representation of the state
        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))

        print("Vehicle Statuses")
        for vs in sorted(self.get_vehicle_statuses()):
            print("    {} is at ({}, {})".format(vs[0], vs[1][0], vs[1][1]), end="")
        board = get_board(self.get_vehicle_statuses(), self.get_board_properties())
        print('\n')
        print('\n'.join([''.join(board[i]) for i in range(len(board))]))

    #Data accessor routines.
    def get_vehicle_statuses(self): 
        '''Return list containing the status of each vehicle
           This list has to be in the format: [vs_1, vs_2, ..., vs_k]
           with one status list for each vehicle in the state.
           Each vehicle status item vs_i is itself a list in the format:
                 [<name>, <loc>, <length>, <is_horizontal>, <is_goal>]
           Where <name> is the name of the robot (a string)
                 <loc> is a location (a pair (x,y)) indicating the front of the vehicle,
                       i.e., its length is counted in the positive x- or y-direction
                       from this point
                 <length> is the length of that vehicle
                 <is_horizontal> is true iff the vehicle is oriented horizontally
                 <is_goal> is true iff the vehicle is a goal vehicle
        '''
        statuses = list()
        for vehicle in self.vehicle_list:
            statuses.append([vehicle.name, vehicle.loc, vehicle.length, vehicle.is_horizontal, vehicle.is_goal])
        return statuses

    def get_board_properties(self): 
        '''Return (board_size, goal_entrance, goal_direction)
           where board_size = (m, n) is the dimensions of the board (m rows, n columns)
                 goal_entrance = (x, y) is the location of the goal
                 goal_direction is one of 'N', 'E', 'S' or 'W' indicating
                                the orientation of the goal
        '''
        return self.board_properties

########################################################
#   Function provided so that you can more easily     #
#   Test your implementation                           #
########################################################
def make_init_state(board_size, vehicle_list, goal_entrance, goal_direction): 
    '''Input the following items which specify a state and return a rushhour object
       representing this initial state.
         The state's g-value is zero
         The state's parent is None
         The state's action is the dummy action "START"
       board_size = (m, n)
          m is the number of rows in the board
          n is the number of columns in the board
       vehicle_list = [v1, v2, ..., vk]
          a list of vehicles. Each vehicle vi is itself a list
          vi = [vehicle_name, (x, y), length, is_horizontal, is_goal] where
              vehicle_name is the name of the vehicle (string)
              (x,y) is the location of that vehicle (int, int)
              length is the length of that vehicle (int)
              is_horizontal is whether the vehicle is horizontal (Boolean)
              is_goal is whether the vehicle is a goal vehicle (Boolean)
      goal_entrance is the coordinates of the entrance tile to the goal and
      goal_direction is the orientation of the goal ('N', 'E', 'S', 'W')
    '''
    return Rushhour('START', 0, None, [board_size, goal_entrance, goal_direction],
        [Vehicle(*v) for v in vehicle_list])

def get_board(vehicle_statuses, board_properties):
    #DO NOT CHANGE THIS FUNCTION
    (m, n) = board_properties[0]
    board = [list(['.'] * n) for i in range(m)]
    for vs in vehicle_statuses:
        for i in range(vs[2]):  # vehicle length
            if vs[3]:
                # vehicle is horizontal
                board[vs[1][1]][(vs[1][0] + i) % n] = vs[0][0]
                # represent vehicle as first character of its name
            else:
                # vehicle is vertical
                board[(vs[1][1] + i) % m][vs[1][0]] = vs[0][0]
                # represent vehicle as first character of its name
    # print goal
    board[board_properties[1][1]][board_properties[1][0]] = board_properties[2]
    return board
