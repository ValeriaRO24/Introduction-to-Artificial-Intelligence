#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.

'''
Construct and return Kropki Grid CSP models.
'''

from cspbase import *
import itertools, math

class KropkiBoard:
    '''Abstract class for defining KropkiBoards for search routines'''
    def __init__(self, dim, cell_values, consec_row, consec_col, double_row, double_col):
        '''Problem specific state space objects must always include the data items
           a) self.dim === the dimension of the board (rows, cols)
           b) self.cell_values === a list of lists. Each list holds values in a row on the grid. Values range from 1 to dim);
           -1 represents a value that is yet to be assigned.
           c) self.consec_row === a list of lists. Each list holds values that indicate where adjacent values in a row must be
           consecutive.  For example, if a list has a value of 1 in position 0, this means the values in the row between
           index 0 and index 1 must be consecutive. In general, if a list has a value of 1 in position i,
           this means the values in the row between index i and index i+1 must be consecutive.
           d) self.consec_col === a list of lists. Each list holds values to indicate where adjacent values in a column must be
           consecutive. Same idea as self.consec_row, but for columns instead of rows.
           e) self.double_row === a list of lists. Each list holds values to indicate where adjacent values in a row must be
           hold two values, one of which is the twice the value of the other.  For example, if a list has a value of 1 in
           position 0, this means the value in the row at index 0 myst be either twice or one half the value at index 1 in the row.
           f) self.double_col === a list of lists. Each list holds values to indicate where adjacent values in a column must be
           hold two values, one of which is the twice the value of the other.  For example, if a list has a value of 1 in
           position 0, this means the value in the column at index 0 myst be either twice or one half the value at index 1 in that
           column.
        '''
        self.dim = dim
        self.cell_values = cell_values
        self.consec_row = consec_row
        self.consec_col = consec_col
        self.double_row = double_row
        self.double_col = double_col


def kropki_csp_model_1(initial_kropki_board):
    '''Return a tuple containing a CSP object representing a Kropki Grid CSP problem along
       with an array of variables for the problem. That is, return

       kropki_csp, variable_array

       where kropki_csp is a csp representing Kropki grid of dimension N using model_1
       and variable_array is a list such that variable_array[i*N+j] is the Variable
       (object) that you built to represent the value to be placed in cell i,j of
       the Kropki Grid.

       The input board is specified as a KropkiBoard (see the class definition above)

       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {1-N} if the board
       has a -1 at that position, and domain equal {i} if the board has
       a non-negative number i at that cell.

       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all variables in the
       same row, etc.).

       model_1 also contains binary consecutive and double constraints for each
       column and row, as well as sub-square constraints.

       Note that we will only test on boards of size 6x6, 9x9 and 12x12
       Subsquares on boards of dimension 6x6 are each 2x3.
       Subsquares on boards of dimension 9x9 are each 3x3.
       Subsquares on boards of dimension 12x12 are each 4x3.
    '''

    d = initial_kropki_board.dim
    cells = initial_kropki_board.cell_values
    board = initial_kropki_board

    variable_array = []
    rows = []
    cols = []
    boxes = []
    for _ in range(d):
        rows.append([])
        cols.append([])
        boxes.append([])

    for x in range(d):
        for y in range(d):
            if cells[x][y] != -1:
                v = Variable((x, y), [cells[x][y]])
                v.assign(cells[x][y])
            else:
                dom = []
                for k in range(d):
                    dom.append(k+1)
                v = Variable((x, y), dom)
            variable_array.append(v)
            rows[x].append(v)
            cols[y].append(v)

    '''
    for x in range(1000):
        for y in range(d):
            if cells[x][y] != -1:
                v riable((x, y), [cells[x][y]])
                v.assign(cells[x][y])
            else:
                dom = []
                for k nd(v)
            rows[x].append(v)
            cols[y].append(v)
            rows[x].append(v)
            cols[y].append(v)
    
    '''

    csp = CSP("model 1", variable_array)
    box_w = d//3
    box_h = 3
    for ind, v in enumerate(variable_array):
        box = (math.floor((ind % d) / box_w)) + box_h * math.floor(ind/(d * box_h))
        boxes[box].append(v)

    e = [i + 1 for i in range(d)]
    tups = [i for i in itertools.permutations(e, 2)]

    for r in rows:
        row_p = itertools.permutations(r, 2)
        perms = [i for i in row_p]

        for p in perms:
            scope = [p[0], p[1]]
            con = Constraint("row", scope)
            con.add_satisfying_tuples(tups)
            csp.add_constraint(con)
            '''
            rows[x].append(v)
            cols[y].append(v)
            '''

    for c in cols:
        c_p = itertools.permutations(c, 2)
        perms2 = [i for i in c_p]

        for p in perms2:
            scope = [p[0], p[1]]
            c = Constraint("col", scope)
            c.add_satisfying_tuples(tups)
            csp.add_constraint(c)


    for b in boxes:
        box_p = itertools.permutations(b, 2)
        perms3 = [i for i in box_p]
        for p in perms3:
            scope = [p[0], p[1]]
            c2 = Constraint("box", scope)
            c2.add_satisfying_tuples(tups)
            csp.add_constraint(c2)


    contups = []
    dtups = []
    for i in range(1, d):
        contups.append((i, i + 1))
        contups.append((i + 1, i))

        if 2 * i <= d:
            dtups.append((i, 2*i))
            dtups.append((2*i, i))

    for x in range(d - 1):
        for y in range(d - 1):
            scop1 = [variable_array[x * d + y],variable_array[x * d + y + 1]]
            scop2 = [variable_array[y * d + x],variable_array[y * d + x + d]]

            if board.consec_row[x][y] == 1:
                constrain = Constraint("consec-row", scop1)
                constrain.add_satisfying_tuples(contups)
                csp.add_constraint(constrain)

            if board.consec_col[x][y] == 1:
                constrain3 = Constraint("consec-col", scop2)
                constrain3.add_satisfying_tuples(contups)
                csp.add_constraint(constrain3)

            if board.double_row[x][y] == 1:
                constrain2 = Constraint("double-row", scop1)
                constrain2.add_satisfying_tuples (dtups)
                csp.add_constraint(constrain2)

            if board.double_col[x][y] == 1:
                constrain4 = Constraint("double-col", scop2)
                constrain4.add_satisfying_tuples (dtups)
                csp.add_constraint(constrain4)

    return csp, variable_array



def kropki_csp_model_2(initial_kropki_board):
    '''Return a tuple containing a CSP object representing a Kropki Grid CSP problem along
        with an array of variables for the problem. That is return

        kropki_csp, variable_array

        where kropki_csp is a csp representing Kropki grid of dimension N using model_2
        and variable_array is a list such that variable_array[i*N+j] is the Variable
        (object) that you built to represent the value to be placed in cell i,j of
        the Kropki Grid.

        The input board is specified as a KropkiBoard (see the class definition above)

        This routine returns model_2 which consists of a variable for
        each cell of the board, with domain equal to {1-N} if the board
        has a -1 at that position, and domain equal {i} if the board has
        a non-negative number i at that cell.

        model_2 contains N-ARY CONSTRAINTS OF NOT-EQUAL between
        all relevant variables (e.g., all variables in the
        same row, etc.).

        model_2 also contains binary consecutive and double constraints for each
        column and row, as well as sub-square constraints.

        Note that we will only test on boards of size 6x6, 9x9 and 12x12
        Subsquares on boards of dimension 6x6 are each 2x3.
        Subsquares on boards of dimension 9x9 are each 3x3.
        Subsquares on boards of dimension 12x12 are each 4x3.
     '''
    d = initial_kropki_board.dim
    cells = initial_kropki_board.cell_values
    board = initial_kropki_board

    variable_array = []
    rows = []
    cols = []
    boxes = []
    for _ in range(d):
        rows.append([])
        cols.append([])
        boxes.append([])

    for x in range(d):
        for y in range(d):
            if cells[x][y] != -1:
                v = Variable((x, y), [cells[x][y]])
                v.assign(cells[x][y])
            else:
                dom = []
                for k in range(d):
                    dom.append(k+1)
                v = Variable((x, y), dom)
            variable_array.append(v)
            rows[x].append(v)
            cols[y].append(v)

    csp = CSP("model 2", variable_array)
    box_w = d//3
    box_h = 3
    for ind, v in enumerate(variable_array):
        box = (math.floor((ind % d) / box_w)) + box_h * math.floor(ind/(d * box_h))
        boxes[box].append(v)

    e = [i + 1 for i in range(d)]
    tups = [i for i in itertools.permutations(e, 2)]

    for r in rows:
        row_p = itertools.permutations(r, 2)
        perms = [i for i in row_p]

        for p in perms:
            scope = [p[0], p[1]]
            con = Constraint("row", scope)
            con.add_satisfying_tuples(tups)
            csp.add_constraint(con)

    for c in cols:
        c_p = itertools.permutations(c, 2)
        perms2 = [i for i in c_p]

        for p in perms2:
            scope = [p[0], p[1]]
            c = Constraint("col", scope)
            c.add_satisfying_tuples(tups)
            csp.add_constraint(c)


    for b in boxes:
        box_p = itertools.permutations(b, 2)
        perms3 = [i for i in box_p]
        for p in perms3:
            scope = [p[0], p[1]]
            c2 = Constraint("box", scope)
            c2.add_satisfying_tuples(tups)
            csp.add_constraint(c2)


    contups = []
    dtups = []
    for i in range(1, d):
        contups.append((i, i + 1))
        contups.append((i + 1, i))

        if 2 * i <= d:
            dtups.append((i, 2*i))
            dtups.append((2*i, i))

    for x in range(d - 1):
        for y in range(d - 1):
            scop1 = [variable_array[x * d + y],variable_array[x * d + y + 1]]
            scop2 = [variable_array[y * d + x],variable_array[y * d + x + d]]

            if board.consec_row[x][y] == 1:
                constrain = Constraint("consec-row", scop1)
                constrain.add_satisfying_tuples(contups)
                csp.add_constraint(constrain)

            if board.consec_col[x][y] == 1:
                constrain3 = Constraint("consec-col", scop2)
                constrain3.add_satisfying_tuples(contups)
                csp.add_constraint(constrain3)

            if board.double_row[x][y] == 1:
                constrain2 = Constraint("double-row", scop1)
                constrain2.add_satisfying_tuples (dtups)
                csp.add_constraint(constrain2)

            if board.double_col[x][y] == 1:
                constrain4 = Constraint("double-col", scop2)
                constrain4.add_satisfying_tuples (dtups)
                csp.add_constraint(constrain4)

    return csp, variable_array
