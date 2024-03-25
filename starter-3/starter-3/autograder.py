from cspbase import *
import itertools
import traceback

from kropki_csp import kropki_csp_model_1, kropki_csp_model_2, KropkiBoard
from propagators import prop_FC,  prop_GAC, ord_mrv

test_ord_mrv = True
test_props = True
test_model = True

b1 = KropkiBoard(6,[[1,6,5,4,-1,3],
       [3,2,6,1,-1,4],
       [4,5,2,3,-1,6],
       [2,1,4,6,-1,5],
       [6,3,1,5,-1,2],
       [5,4,3,2,-1,1]],
       [[0,1,1,0,1],[1,0,0,0,1],[1,0,1,0,0],[0,0,0,0,0],[0,0,0,1,0],[1,1,1,0,0]],
       [[0,1,0,0,1],[0,0,0,0,1],[1,0,0,0,0],[0,0,0,1,0],[0,0,0,1,0],[1,0,1,0,0]],
       [[0,0,0,1,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,1,0],[1,0,0,0,1],[0,0,0,0,0]],
       [[0,0,1,0,0],[0,0,0,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,0,0,0],[0,0,0,0,0]])

b1sol = KropkiBoard(6,[[1,6,5,4,2,3],
       [3,2,6,1,5,4],
       [4,5,2,3,1,6],
       [2,1,4,6,3,5],
       [6,3,1,5,4,2],
       [5,4,3,2,6,1]],
       [[0,1,1,0,1],[1,0,0,0,1],[1,0,1,0,0],[0,0,0,0,0],[0,0,0,1,0],[1,1,1,0,0]],
       [[0,1,0,0,1],[0,0,0,0,1],[1,0,0,0,0],[0,0,0,1,0],[0,0,0,1,0],[1,0,1,0,0]],
       [[0,0,0,1,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,1,0],[1,0,0,0,1],[0,0,0,0,0]],
       [[0,0,1,0,0],[0,0,0,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,0,0,0],[0,0,0,0,0]])

b2 = KropkiBoard(6,[[-1,-1,-1,-1,-1,-1],
       [-1,-1,-1,-1,-1,-1],
       [-1,-1,-1,-1,-1,-1],
       [-1,-1,-1,-1,-1,-1],
       [-1,-1,-1,-1,-1,-1],
       [-1,-1,-1,-1,-1,-1]],
       [[0,0,1,0,0],[0,1,0,0,0],[0,0,0,0,0],[1,0,0,1,0],[1,0,0,0,0],[1,0,1,0,0]],
       [[0,1,0,0,0],[0,0,1,1,0],[0,1,0,0,0],[0,0,0,1,0],[0,1,1,0,0],[0,0,1,0,1]],
       [[0,0,0,1,0],[1,0,0,1,0],[1,0,0,0,0],[0,0,0,0,0],[0,1,0,1,0],[0,0,0,0,0]],
       [[0,0,1,0,0],[0,0,0,0,0],[0,0,0,0,1],[1,1,0,0,1],[1,0,0,1,0],[0,0,0,0,0]])

b2sol = KropkiBoard(6,[[5,1,3,4,2,6],
       [3,6,5,2,4,1],
       [2,4,6,1,5,3],
       [4,3,1,5,6,2],
       [1,2,4,6,3,5],
       [6,5,2,3,1,4]],
       [[0,0,1,0,0],[0,1,0,0,0],[0,0,0,0,0],[1,0,0,1,0],[1,0,0,0,0],[1,0,1,0,0]],
       [[0,1,0,0,0],[0,0,1,1,0],[0,1,0,0,0],[0,0,0,1,0],[0,1,1,0,0],[0,0,1,0,1]],
       [[0,0,0,1,0],[1,0,0,1,0],[1,0,0,0,0],[0,0,0,0,0],[0,1,0,1,0],[0,0,0,0,0]],
       [[0,0,1,0,0],[0,0,0,0,0],[0,0,0,0,1],[1,1,0,0,1],[1,0,0,1,0],[0,0,0,0,0]])

def queensCheck(qi, qj, i, j):
    '''Return true if i and j can be assigned to the queen in row qi and row qj
       respectively. Used to find satisfying tuples.
    '''
    return i != j and abs(i-j) != abs(qi-qj)

def nQueens(n):
    '''Return an n-queens CSP'''
    i = 0
    dom = []
    for i in range(n):
        dom.append(i+1)

    vars = []
    for i in dom:
        vars.append(Variable('Q{}'.format(i), dom))

    cons = []
    for qi in range(len(dom)):
        for qj in range(qi+1, len(dom)):
            con = Constraint("C(Q{},Q{})".format(qi+1,qj+1),[vars[qi], vars[qj]])
            sat_tuples = []
            for t in itertools.product(dom, dom):
                if queensCheck(qi, qj, t[0], t[1]):
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

    csp = CSP("{}-Queens".format(n), vars)
    for c in cons:
        csp.add_constraint(c)
    return csp

##Tests FC after the first queen is placed in position 1.
def test_simple_FC():
    did_fail = False
    score = 0
    try:
        queens = nQueens(8)
        curr_vars = queens.get_all_vars()
        curr_vars[0].assign(1)
        prop_FC(queens,newVar=curr_vars[0])
        answer = [[1],[3, 4, 5, 6, 7, 8],[2, 4, 5, 6, 7, 8],[2, 3, 5, 6, 7, 8],[2, 3, 4, 6, 7, 8],[2, 3, 4, 5, 7, 8],[2, 3, 4, 5, 6, 8],[2, 3, 4, 5, 6, 7]]
        var_domain = [x.cur_domain() for x in curr_vars]
        for i in range(len(curr_vars)):
            if var_domain[i] != answer[i]:
                details = "Failed simple FC test: variable domains don't match expected results"
                did_fail = True
                break
        if not did_fail:
            score = 1
            details = ""
    except Exception:
        details = "One or more runtime errors occurred while testing simple FC: %r" % traceback.format_exc()

    return score,details

##Tests GAC after the first queen is placed in position 1.
def test_simple_GAC():
    did_fail = False
    score = 0
    try:
        queens = nQueens(8)
        curr_vars = queens.get_all_vars()
        curr_vars[0].assign(1)
        prop_GAC(queens,newVar=curr_vars[0])
        answer = [[1],[3, 4, 5, 6, 7, 8],[2, 4, 5, 6, 7, 8],[2, 3, 5, 6, 7, 8],[2, 3, 4, 6, 7, 8],[2, 3, 4, 5, 7, 8],[2, 3, 4, 5, 6, 8],[2, 3, 4, 5, 6, 7]]
        var_domain = [x.cur_domain() for x in curr_vars]
        print(var_domain)
        print(answer)
        for i in range(len(curr_vars)):
            if var_domain[i] != answer[i]:
                details = "Failed simple GAC test: variable domains don't match expected results."
                did_fail = True
                break
        if not did_fail:
            score = 1
            details = ""

    except Exception:
        details = "One or more runtime errors occurred while testing simple GAC: %r" % traceback.format_exc()

    return score,details

def three_queen_GAC():
    score = 0
    try:
        queens = nQueens(8)
        curr_vars = queens.get_all_vars()
        curr_vars[0].assign(4)
        curr_vars[2].assign(1)
        curr_vars[7].assign(5)
        prop_GAC(queens)
        answer = [[4],[6, 7, 8],[1],[3, 8],[6, 7],[2, 8],[2, 3, 7, 8],[5]]
        var_vals = [x.cur_domain() for x in curr_vars]

        print(var_vals)
        print(answer)
        if var_vals != answer:
            details = "Failed three queens GAC test: variable domains don't match expected results"

        else:
            score = 1
            details = ""
    except Exception:
        details = "One or more runtime errors occurred while testing GAC with three queens: %r" % traceback.format_exc()

    return score,details

def three_queen_FC():
    score = 0
    try:
        queens = nQueens(8)
        curr_vars = queens.get_all_vars()
        curr_vars[0].assign(4)
        curr_vars[2].assign(1)
        curr_vars[7].assign(5)
        prop_FC(queens)

        answer = [[4],[6, 7, 8],[1],[3, 6, 8],[6, 7],[2, 6, 8],[2, 3, 7, 8],[5]]
        var_vals = [x.cur_domain() for x in curr_vars]

        if var_vals != answer:
            details = "Failed three queens FC test: variable domains don't match expected results"

        else:
            score = 1
            details = ""

    except Exception:
        details = "One or more runtime errors occurred while testing FC with three queens: %r" % traceback.format_exc()

    return score,details

def print_kropki_soln(var_array, dim):
    c = 1
    for var in var_array:
        print(var.get_assigned_value(), end=" ")
        if c%dim == 0 and c != 0:
            print("\n")
        c += 1

def check_solution(var_array, kropki_board_soln):


    count, rcount = 0, 0
    dim = kropki_board_soln.dim
    row = kropki_board_soln.cell_values[count]
    for var in var_array:

        if int(var.get_assigned_value()) != row[rcount]: return 0
        else: rcount += 1
        if rcount == dim:
            count += 1
            if count < dim: row = kropki_board_soln.cell_values[count]
            rcount = 0

    return 1

def test_ord_mrv_fun():

    a = Variable('A', [1])
    b = Variable('B', [1])
    c = Variable('C', [1])
    d = Variable('D', [1])
    e = Variable('E', [1])

    simpleCSP = CSP("Simple", [a,b,c,d,e])

    count = 0
    for i in range(0,len(simpleCSP.vars)):
        simpleCSP.vars[count].add_domain_values(range(0, count))
        count += 1

    var = ord_mrv(simpleCSP)

    if var:
        if var.name == simpleCSP.vars[0].name: return 1

    return 0

if __name__ == "__main__":

    if test_model:
        print("\n\n********************************************\n")
        print("MODEL TESTS\n")
        print("********************************************\n")

        total = 0
        c=0
        for b in [b1, b2]:

            if c == 0: sol = b1sol
            else: sol = b2sol

            print("Solving board .... ")

            print("Using Model 1")
            csp, var_array = kropki_csp_model_1(b)

            if csp != None:
                solver = BT(csp)
                print("=======================================================")
                print("GAC")
                solver.bt_search(prop_GAC, var_ord=ord_mrv)
                #print("Solution") #if you want to see the solution, uncomment here
                #print_kropki_soln(var_array, b.dim)

                total += check_solution(var_array, sol)

            print("Using Model 2")
            csp, var_array = kropki_csp_model_2(b)
            if csp != None:
                solver = BT(csp)
                print("=======================================================")
                print("FC")
                solver.bt_search(prop_FC, var_ord=ord_mrv)
                #print("Solution") #if you want to see the solution, uncomment here
                #print_kropki_soln(var_array, b.dim)
                total += check_solution(var_array, sol)
            c += 1

        print("\n\n********************************************\n")
        print("Total model tests passed: %d/4\n" % total)
        print("********************************************\n")

    if test_props:
        total = 0
        print("\n\n********************************************\n")
        print("PROPAGATOR TESTS\n")
        print("********************************************\n")

        print("---starting test_simple_FC---")
        score,details = test_simple_FC()
        total += score
        print(details)
        print("---finished test_simple_FC---\n")

        print("---starting test_simple_GAC---")
        score,details = test_simple_GAC()
        total += score
        print(details)
        print("---finished test_simple_GAC---\n")

        print("---starting three_queen_FC---")
        score,details = three_queen_FC()
        total += score
        print(details)
        print("---finished three_queen_FC---\n")

        print("---starting three_queen_GAC---")
        score,details = three_queen_GAC()
        total += score
        print(details)
        print("---finished three_queen_GAC---\n")

        print("\n\n********************************************\n")
        print("Total propagator tests passed: %d/4\n" % total)
        print("********************************************\n")

    if test_ord_mrv:
        print("\n\n********************************************\n")
        print("ORDERING TESTS\n")
        print("********************************************\n")
        score = test_ord_mrv_fun()
        print("\n\n********************************************\n")
        print("Total MRV tests passed: %d/1\n" % score)
        print("********************************************\n")
