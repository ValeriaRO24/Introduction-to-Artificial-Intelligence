#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.
'''
This file will contain different constraint propagators to be used within
bt_search.

propagator == a function with the following template
    propagator(csp, newly_instantiated_variable=None)
        ==> returns (True/False, [(Variable, Value), (Variable, Value) ...])

    csp is a CSP object---the propagator can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    newly_instaniated_variable is an optional argument.
    if newly_instantiated_variable is not None:
        then newly_instantiated_variable is the most
        recently assigned variable of the search.
    else:
        propagator is called before any assignments are made
        in which case it must decide what processing to do
        prior to any variables being assigned. SEE BELOW

    The propagator returns True/False and a list of (Variable, Value) pairs.

    Returns False if a deadend has been detected by the propagator.
        in this case bt_search will backtrack
    Returns True if we can continue.

    The list of variable values pairs are all of the values
    the propagator pruned (using the variable's prune_value method).
    bt_search NEEDS to know this in order to correctly restore these
    values when it undoes a variable assignment.

    NOTE propagator SHOULD NOT prune a value that has already been
    pruned! Nor should it prune a value twice.

    IF PROPAGATOR is called with newly_instantiated_variable = None
        PROCESSING REQUIRED:
            for plain backtracking (where we only check fully instantiated
            constraints) we do nothing...return (true, [])

            for forward checking (where we only check constraints with one
            remaining variable) we look for unary constraints of the csp
            (constraints whose scope contains only one variable) and we
            forward_check these constraints.

            for gac we establish initial GAC by initializing the GAC queue with
            all constaints of the csp

    IF PROPAGATOR is called with newly_instantiated_variable = a variable V
        PROCESSING REQUIRED:
            for plain backtracking we check all constraints with V (see csp
            method get_cons_with_var) that are fully assigned.

            for forward checking we forward check all constraints with V that
            have one unassigned variable left

            for gac we initialize the GAC queue with all constraints containing
            V.
'''
def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''
    no_deadend = True #False if and only if a dead-end is found
    dead_end = False
    pruned_list = []
   # all_vars = csp.get_all_vars()
   # all_cons = csp.get_all_cons()
    if newVar:
        for c in csp.get_cons_with_var(newVar):
            '''
            thought process: first check with new var if exists and do the FC with 
            the var so 
            
            CSP METHOD get_cons_with_var
            
            '''
            if c.get_n_unasgn() == 1:

                unassigned_var = c.get_unasgn_vars()[0]
                temp = []
                for v in c.get_scope():
                    if v != unassigned_var:
                        temp.append(v.get_assigned_value())

                for x in unassigned_var.cur_domain():
                    temp.append(x)
                    '''
                    have temp for now, maybe change later, change for unassigned var
                    '''


                    if not c.check(temp):

                        unassigned_var.prune_value(x)
                        pruned_list.append((unassigned_var, x))


                    temp.remove(x)
                    if not unassigned_var.cur_domain:
                        return dead_end, pruned_list
    else:
        for c in csp.get_all_cons():
            if c.get_n_unasgn() == 1:
                '''
                Now to without newvar because doesnt exist
                
                CSP METHOD csp.get_all_cons
                
                
                
                '''


                unassigned_var = c.get_unasgn_vars()[0]
                temp = []
                for v in c.get_scope():
                    if v != unassigned_var:

                        temp.append(v.get_assigned_value())
                for x in unassigned_var.cur_domain():


                    temp.append(x)
                    if not c.check(temp) :
                        unassigned_var.prune_value(x)


                        pruned_list.append((unassigned_var, x))
                    temp.remove(x)

                    if not unassigned_var.cur_domain:
                        return dead_end, pruned_list

    return no_deadend, pruned_list

def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    pruned_list = []

    if newVar:
        GAC_queue = csp.get_cons_with_var(newVar)
        while GAC_queue:
            c = GAC_queue.pop(0)
            for v in c.get_scope():

                for x in v.cur_domain():
                    if not c.has_support(v, x):
                        v.prune_value(x)


                        pruned_list.append((v, x))
                        '''
                        CHECK pruned list, ---> do the pycharm debug, check variables 
                        
                        FIX bug with first part
                        
                        
                        '''



                        if not v.cur_domain():
                            return False, pruned_list

                        v_cons = csp.get_cons_with_var(v)
                        for i in v_cons:
                            if i not in GAC_queue and i != c:
                                GAC_queue.append(i)

    else:
        GAC_queue = csp.get_all_cons()
        while GAC_queue:
            c = GAC_queue.pop(0)
            '''
            not pruned list 
            '''

            for v in c.get_scope():
                for x in v.cur_domain():
                    '''
                    if c.has_support(v, x):
                    add to not pruned list and then compare
                        v.prune_value(x)
                        pruned_list.append((v, x))
                    '''



                    if not c.has_support(v, x):
                        v.prune_value(x)
                        pruned_list.append((v, x))
                        if not v.cur_domain():
                            return False, pruned_list


                        v_cons = csp.get_cons_with_var(v)



                        for i in v_cons:
                            if i not in GAC_queue and i != c:
                                GAC_queue.append(i)

    return True, pruned_list
def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    v = csp.get_all_unasgn_vars()
    min = v[0].cur_domain_size()




    curr_v = v[0]
    '''
    for i in v:
        if i.cur_domain_size() < min:
            min = i.cur_domain_size()
    '''


    for i in v:
        if i.cur_domain_size() < min:
            min = i.cur_domain_size()
            curr_v = i

    return curr_v
