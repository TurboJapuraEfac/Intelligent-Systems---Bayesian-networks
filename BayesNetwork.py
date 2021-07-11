from itertools import product

class BayesianNetwork(object):
    def __init__(self, structure, probabilityValues, queries):
        self.variables = structure["variables"]
        self.dependencies = structure["dependencies"]
        self.conditional_probabilities = probabilityValues["conditional_probabilities"]
        self.prior_probabilities = probabilityValues["prior_probabilities"]
        self.queries = queries
        self.graph = {}

    def createPriorProbTable(self, var):
        value_dict = self.prior_probabilities[var]
        prob_table = {}
        for key in value_dict:
            prob_table[key] = value_dict[key]
        return prob_table

    def createConditionalProbTable(self, var):
        value_dict_arr = self.conditional_probabilities[var]
        prob_table = {}
        for value_dict in value_dict_arr:
            prob = value_dict['probability']
            key = ()
            for k in value_dict:
                if k != 'probability':
                    if k != 'own_value':
                        key = key + ((k, value_dict[k]),)
                    else:
                        key = key + ((var, value_dict[k]),)
            key = tuple(sorted(key))
            prob_table[key] = prob
        return prob_table

    def makeGraph(self):
        for var in self.variables:
            node = Node(var)
            self.graph[var] = node

        for var in self.prior_probabilities:
            self.graph[var].setProbabilityTable(self.createPriorProbTable(var))
            self.graph[var].setIsPrior(True)

        for var in self.dependencies:
            parents = self.dependencies[var]
            self.graph[var].addParents(parents)
            self.graph[var].setProbabilityTable(self.createConditionalProbTable(var))
            self.graph[var].setIsPrior(False)
            for p in parents:
                self.graph[p].addChild(var)

    def permutations(self, tab, length):
        return list(product([True, False], repeat=length))

    def inference(self):
        given = self.queries["given"]
        tofind = self.queries["tofind"]
        fixedVariables = [x for x in given] + [x for x in tofind]
        varyingVariables = [y for y in self.variables if y not in fixedVariables]
        p1 = self.getProbability(given, tofind, fixedVariables, varyingVariables)

        print("P(", fixedVariables[-1], end=" | ")
        for index in range(len(fixedVariables) - 1):
            if len(fixedVariables) - 2 == index:
                print(fixedVariables[index], end="")
            else:
                print(fixedVariables[index], end=",")
        print(")", end=' = ')

        fixedVariables = [x for x in given]
        varyingVariables = list(set([y for y in self.variables if y not in fixedVariables] + [x for x in tofind]))
        p2 = self.getProbability(given, tofind, fixedVariables, varyingVariables)
        ans = p1 / p2
        print(ans)

    def probabilityValues(self, arr):
        sum = 0
        for i in arr:
            prod = 1
            for j in i:
                prod *= j
            sum += prod
        return sum

    def returnAllProbabilities(self, value_dict):
        prob_arr = []
        for var in self.graph:
            node = self.graph[var]
            prob_arr.append(node.getProb(value_dict))
        return prob_arr

    def getProbability(self, given, tofind, fixedVariables, varyingVariables):
        all_prob = []
        table_of_variables = given.copy()
        table_of_variables.update(tofind)
        for var in varyingVariables:
            table_of_variables[var] = 'True'
        all_possible_truth_probabilityValues = self.permutations(table_of_variables, len(varyingVariables))
        for iteration in range(2 ** len(varyingVariables)):
            current_truth_probabilityValues = all_possible_truth_probabilityValues[iteration]
            for index, var in enumerate(varyingVariables):
                table_of_variables[var] = str(current_truth_probabilityValues[index])
            prob = self.returnAllProbabilities(table_of_variables)
            all_prob.extend([prob]) 
        prob = self.probabilityValues(all_prob)
        return prob


class Node:
    def __init__(self, name):
        self.parents = []
        self.children = []
        self.name = name
        self.isPrior = True
        self.prob_table = {}

    def addChild(self, child):
        self.children.append(child)

    def addParents(self, parents):
        self.parents.extend(parents)

    def setIsPrior(self, isPrior):
        self.isPrior = isPrior

    def setProbabilityTable(self, prob_table):
        self.prob_table = prob_table

    def isPrior(self):
        return self.isPrior

    def getProb(self, value_dict):
        if self.isPrior:
            key = value_dict[self.name]
        else:
            condition = self.parents + [self.name]
            key = ()
            for c in condition:
                key = key + ((c, value_dict[c]),)
            key = tuple(sorted(key))
        return self.prob_table[key]

