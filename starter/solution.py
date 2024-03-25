from bnetbase import Variable, Factor, BN, adultDatasetBN
import itertools
import csv

def multiply_factors(Factors):
    '''return a new factor that is the product of the factors in Fators
    @return a factor'''
    product_factors = Factor(Factors[0].name, Factors[0].scope)
    product_factors.values = Factors[0].values.copy()

    for factor in Factors[1:]:
        product_factors = multiply_helper(product_factors, factor)

    return product_factors

def multiply_helper(f1, f2):
    new_scope = f1.get_scope().copy()
    f1_dom = []
    f2_dom = []
    doms = []
    pro_vals = []

    for i in f2.get_scope():
        if i not in new_scope:
            new_scope.append(i)

    new_product = Factor("product of " + str(f1.name) + " and " + str(f2.name), new_scope)

    for v in f1.get_scope():
        f1_dom.extend(v.domain())
    for v in f2.get_scope():
        f2_dom.extend(v.domain())
    for v in new_scope:
        doms.append(v.domain())

    value_combs = list(itertools.product(*doms))
    value_combs = list((list(tup) for tup in value_combs))

    for c in value_combs:
        f1_v = []
        f2_v = []
        for v in c:
            if v in f1_dom:
                f1_v.append(v)
            if v in f2_dom:
                f2_v.append(v)

        new_order1 = []
        new_order2 = []
        for variable in f1.get_scope():
            for var in f1_v:
                if var in variable.domain():
                    new_order1.append(var)

        for variable in f2.get_scope():
            for var in f2_v:
                if var in variable.domain():
                    new_order2.append(var)

        prob1 = f1.get_value(new_order1)
        prob2 = f2.get_value(new_order2)
        pro_vals.append([*c, prob1 * prob2])
    new_product.add_values(pro_vals)
    return new_product



def restrict_factor(f, var, value):
    '''f is a factor, var is a Variable, and value is a value from var.domain.
    Return a new factor that is the restriction of f by this var = value.
    Don't change f! If f has only one variable its restriction yields a
    constant factor
    @return a factor'''

    res_factor = Factor("restricted " + str(var.name), f. get_scope())
    vals = []
    dom = []

    for v in res_factor.get_scope():
        if v == var:
            v.set_assignment(value)

    for v in f.get_scope():
        dom.append(v.domain())

    value_combs = list(itertools.product(*dom))
    value_combs = list((list (tup) for tup in value_combs))

    for c in value_combs:
        if value in c:
            vals.append([*c, f.get_value(c)])

    res_factor.add_values(vals)

    return res_factor




def sum_out_variable(f, var):
    '''return a new factor that is the product of the factors in Factors
       followed by the suming out of Var
    @return a factor'''

    vals = []

    dom = []
    for v in f.get_scope():
        if v != var:
            dom.append(v.domain())

    sfactor = Factor("summed out " + str(var.name), f. get_scope())
    sfactor.scope.remove(var)

    i = f.get_scope().index(var)
    value_combs = list(itertools.product(*dom))
    value_combs = list((list(tup) for tup in value_combs))

    for val in value_combs:
        s = 0
        for x in var.domain():
            v = val[:i] + [x] + val[i:]
            s += f.get_value(v)
        vals.append(val + [s])


    sfactor.add_values(vals)
    return sfactor




def normalize(nums):
    '''take as input a list of number and return a new list of numbers where
    now the numbers sum to 1, i.e., normalize the input numbers
    @return a normalized list of numbers'''
    total = 0
    for n in nums:
        total += abs(n)




    normalized_lst = []
    if total == 0:
        for n in nums:
            normalized_lst.append((1/len(nums)))
        return normalized_lst

    for n in nums:
        normalized_lst.append((abs(n)/total))



    return normalized_lst

def min_fill_ordering(Factors, QueryVar):
    '''Compute an elimination order given a list of factors using the min fill heuristic.
    Variables in the list will be derived from the scopes of the factors in Factors.
    Order the list such that the first variable in the list generates the smallest
    factor upon elimination. The QueryVar must NOT part of the returned ordering using.
    @return a list of variables'''
    ### YOUR CODE HERE ###
    vars = []
    x = []
    for fact in Factors:
        for v in fact.get_scope():
            if v not in vars and v != QueryVar:
                vars.append(v)

    for v in vars:
        count = 0
        for f in Factors:
            if v in f.get_scope():
                count += 1
        x.append([count, v])

    x.sort(key = lambda y: y[0])
    output = [z[1] for z in x]
    return output


###
def VE(Net, QueryVar, EvidenceVars):
    '''
    Input: Net---a BN object (a Bayes Net)
           QueryVar---a Variable object (the variable whose distribution
                      we want to compute)
           EvidenceVars---a LIST of Variable objects. Each of these
                          variables has had its evidence set to a particular
                          value from its domain using set_evidence.

   VE returns a distribution over the values of QueryVar, i.e., a list
   of numbers one for every value in QueryVar's domain. These numbers
   sum to one, and the i'th number is the probability that QueryVar is
   equal to its i'th value given the setting of the evidence
   variables. For example if QueryVar = A with Dom[A] = ['a', 'b',
   'c'], EvidenceVars = [B, C], and we have previously called
   B.set_evidence(1) and C.set_evidence('c'), then VE would return a
   list of three numbers. E.g. [0.5, 0.24, 0.26]. These numbers would
   mean that Pr(A='a'|B=1, C='c') = 0.5 Pr(A='a'|B=1, C='c') = 0.24
   Pr(A='a'|B=1, C='c') = 0.26
    @return a list of probabilities, one for each item in the domain of the QueryVar'''

    facts = Net.factors()
    for i, f in enumerate(facts):
        for evar in EvidenceVars:
            if evar in f.get_scope():
                facts[i] = restrict_factor(f, evar, evar.get_evidence())
    order = min_fill_ordering(facts, QueryVar)

    for var in order:
        f_vars = [f for f in facts if var in f.get_scope()]
        facts = [f for f in facts if f not in f_vars]
        product = multiply_factors(f_vars)
        new_f = sum_out_variable(product, var)
        facts.append(new_f)

    x_factor = multiply_factors(facts)
    p = normalize(x_factor.values)

    return p


def NaiveBayesModel():
    '''
   NaiveBayesModel returns a BN that is a Naive Bayes model that
   represents the joint distribution of value assignments to
   variables in the Adult Dataset from UCI.  Remember a Naive Bayes model
   assumes P(X1, X2,.... XN, Class) can be represented as
   P(X1|Class)*P(X2|Class)* .... *P(XN|Class)*P(Class).
   When you generated your Bayes Net, assume that the values
   in the SALARY column of the dataset are the CLASS that we want to predict.
   @return a BN that is a Naive Bayes model and which represents the Adult Dataset.
    '''
    ### READ IN THE DATA
    input_data = []
    with open('data/adult-dataset.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None) #skip header row
        for row in reader:
            input_data.append(row)

    ### DOMAIN INFORMATION REFLECTS ORDER OF COLUMNS IN THE DATA SET
    variable_domains = {
    "MaritalStatus": ['Not-Married', 'Married', 'Separated', 'Widowed'],
    "Relationship": ['Wife', 'Own-child', 'Husband', 'Not-in-family', 'Other-relative', 'Unmarried'],
    "Race": ['White', 'Black', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other'],
    "Gender": ['Male', 'Female'],
    "Occupation": ['Admin', 'Military', 'Manual Labour', 'Office Labour', 'Service', 'Professional'],
    "Country": ['North-America', 'South-America', 'Europe', 'Asia', 'Middle-East', 'Carribean'],
    "Education": ['<Gr12', 'HS-Graduate', 'Associate', 'Professional', 'Bachelors', 'Masters', 'Doctorate'],
    "Work": ['Not Working', 'Government', 'Private', 'Self-emp'],
    "Salary": ['<50K', '>=50K']
    }
    ### YOUR CODE HERE ###
    variables = []
    factors = []
    count = len(input_data)
    salary = {'<50K':0, '>=50K':0}
    for var in variable_domains.keys():
        variables.append(Variable(var, variable_domains[var]))


    for row in input_data:
        if row[8] in salary:
            salary[row[8]] += 1


    s = Factor('P(sa)', [variables[-1]])
    s.add_values([['<50K', salary['<50K']/count], ['>=50K', salary['>=50K']/count]])

    factors.append(s)

    country = Factor('P(co|sa)', [variables[5], variables [8]])
    country.add_values(count_sal(input_data, variable_domains, "Country", 7, salary))
    factors.append(country)

    gender = Factor('P(ge|sa)', [variables[3], variables [8]])
    gender.add_values(count_sal(input_data, variable_domains, "Gender", 6, salary))
    factors.append(gender)

    relationship = Factor('P(re|sa)', [variables[1], variables [8]])
    relationship.add_values(count_sal(input_data, variable_domains, "Relationship", 4, salary))
    factors.append(relationship)

    occupation = Factor('P(occ|sa)', [variables[4], variables [8]])
    occupation.add_values(count_sal(input_data, variable_domains, "Occupation", 3, salary))
    factors.append(occupation)

    maritalStatus = Factor('P(ms|sa)', [variables[0], variables [8]])
    maritalStatus.add_values(count_sal(input_data, variable_domains, "MaritalStatus", 2, salary))
    factors.append(maritalStatus)

    education = Factor('P(ed|sa)', [variables[6], variables [8]])
    education.add_values(count_sal(input_data, variable_domains, "Education", 1, salary))
    factors.append(education)

    work = Factor('P(wo|sa)', [variables[7], variables [8]])
    work.add_values(count_sal(input_data, variable_domains, "Work", 0, salary))
    factors.append(work)

    race = Factor('P(rc|sa)', [variables[2], variables [8]])
    race.add_values(count_sal(input_data, variable_domains, "Race", 5, salary))
    factors.append(race)

    return BN("adult data set BN", variables, factors)

def count_sal(data, var_dom, name, i, sal):
    sdomain = var_dom[ "Salary"]
    vdomain = var_dom[name]

    domain = list(itertools.product(vdomain, sdomain))
    domain = list((list(tup) for tup in domain))

    for v in domain:
        v.append(0)

    for row in data:
        for v in domain:
            if row[-1] == v[1] and row[i] == v[0]:
                v[2] += 1

    for v in domain:
        v[2] = v[2]/sal[v[1]]

    return domain





def explore(Net, question):
    '''    Input: Net---a BN object (a Bayes Net)
           question---an integer indicating the question in HW4 to be calculated. Options are:
           1. What percentage of the women in the data set end up with a P(S=">=$50K"|E1) that is strictly greater than P(S=">=$50K"|E2)?
           2. What percentage of the men in the data set end up with a P(S=">=$50K"|E1) that is strictly greater than P(S=">=$50K"|E2)?
           3. What percentage of the women in the data set with P(S=">=$50K"|E1) > 0.5 actually have a salary over $50K?
           4. What percentage of the men in the data set with P(S=">=$50K"|E1) > 0.5 actually have a salary over $50K?
           5. What percentage of the women in the data set are assigned a P(Salary=">=$50K"|E1) > 0.5, overall?
           6. What percentage of the men in the data set are assigned a P(Salary=">=$50K"|E1) > 0.5, overall?
           @return a percentage (between 0 and 100)
    '''
    input_data = []
    with open('data/adult-dataset.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None) #skip header row
        for row in reader:
            input_data.append(row)

    if question == 1:
        count = 0
        total_data = len(input_data)
        for row in input_data:
            if row[6] == "Female":
                QV = Net.get_variable("Salary")
                e1, e2 = evidence(Net, row)
                p1 = VE(Net, QV, e1)
                p2 = VE(Net, QV, e2)

                if p1[1] > p2[1]:
                    count += 1

        return count/total_data * 100

    elif question == 2:

        count = 0
        total_data = len(input_data)
        for row in input_data:
            if row[6] == "Male":
                QV = Net.get_variable("Salary")
                e1, e2 = evidence(Net, row)
                p1 = VE(Net, QV, e1)
                p2 = VE(Net, QV, e2)

                if p1[1] > p2[1]:
                    count += 1

        return count/total_data * 100

    elif question == 3:

        count = 0
        total = 0
        for row in input_data:
            if row[6] == "Female":
                QV = Net.get_variable("Salary")
                e1, e2 = evidence(Net, row)
                p1 = VE(Net, QV, e1)


                if p1[1] > 0.5:
                    total +=1
                    if row[8] == '>=50k':
                        count += 1

        return count/total * 100

    elif question == 4:

        count = 0
        total = 0
        for row in input_data:
            if row[6] == "Male":
                QV = Net.get_variable("Salary")
                e1, e2 = evidence(Net, row)
                p1 = VE(Net, QV, e1)


                if p1[1] > 0.5:
                    total +=1
                    if row[8] == '>=50k':
                        count += 1

        return count/total * 100

    elif question == 5:

        count = 0
        total = 0
        for row in input_data:
            if row[6] == "Female":
                total += 1
                QV = Net.get_variable("Salary")
                e1, e2 = evidence(Net, row)
                p1 = VE(Net, QV, e1)


                if p1[1] > 0.5:
                        count += 1

        return count/total * 100

    elif question == 6:

        count = 0
        total = 0
        for row in input_data:
            if row[6] == "Male":
                total += 1
                QV = Net.get_variable("Salary")
                e1, e2 = evidence(Net, row)
                p1 = VE(Net, QV, e1)


                if p1[1] > 0.5:
                    count += 1

        return count/total * 100


def evidence(Net, r):
    e1 = []
    e2 = []

    work = Net.get_variable("Work")
    work.set_evidence(r[0])
    e1.append(work)
    e2.append(work)

    occ = Net.get_variable("Occupation")
    occ.set_evidence(r[3])
    e1.append(occ)
    e2.append(occ)

    ed = Net.get_variable("Education")
    ed.set_evidence(r[1])
    e1.append(ed)
    e2.append(ed)

    re = Net.get_variable("Relationship")
    re.set_evidence(r[4])
    e1.append(re)
    e2.append(re)

    ge = Net.get_variable("Gender")
    ge.set_evidence(r[6])
    e2.append(ge)

    return e1, e2










