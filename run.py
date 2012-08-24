#!/usr/bin/en python

from dt import DecisionTree

class Reader():
    def __init__(self, file)
        pass

class VariableIndex(object):
    def __init__(self, examples):
        self.variables = {}
        for example in examples:
            for attribute, value in example:
                if self.variables.has_key(attribute):
                    if not value in self.variables[attribute]:
                        self.variables[attribute].append(value)
                else:
                    self.variables[attribute] = [value]

    def __getattribute__(self, name):
       return self.variables[name] 


class CountIndex():
    def __init__(self, examples):
        for example in examples:
            for var, val in example.items():
                if self.values.has_key(var):
                    self.values[var] = self.values[var] + 1
                else: 
                    self.values[var] = 1

    def __getattribute__(self, name):
        self.variables[name]

#{poisonouse: 0, capshape: 'f', etc}
class Node():
    def __init__(self, examples):
        self.leaves = examples
        self._attributes = False

    def __len__(self):
        len(self.leaves)


    @attribute
    def attributes(self):
        """ RETURN a set of tuples of keys and values for each attributes """
        if self._attributes
            return self._attributes
        
        attrs = {}

        for leaf in self.leaves:
            for attribute, value in leaf:
                if attrs.has_key(attribute):
                    if not value in attrs[attribute]
                        attrs[attribute.append(value)]

                else:
                    attrs[attribute] = [value]

        self._attributes = attrs

        return self._attributes


    def information_gain(self, attr):
        """ 
        Calculate the IG of the leaves accross attr
        IG(poisonous, attr) = H(poisonous) - H(pointnous|attributes)
        """
        return self.entropy("poisonous") - self.conditional_entropy("poisonous", attr)


    def entropy(self, attribute):
        """
        H(X) = sum[p(x)*log(px)]
        """

    def prob(self, variable, value):
        """
        probability of args
        """
        nume = len([1 for x in self.examples if x[variable] == value])
        return  nume / len(self.examples)


    def joint_prob(self, v_a, i_a, v_b, i_b):
        nume = len([1 for x in self.examples if x[v_a] == i_a and x[v_b] == i_b])

        return nume / len(self.examples)

        
    def conditional_entropy(self, attr_a, attr_b):
        """
        H(Y|X) = sum[p(x,y)*log(p(y)/p(x,y))]
        """

        total = 0
        for attr_a_value in self.attributes[attr_a]:
            p_y = self.prob(attr_a, attr_a_value)
            for attr_b_value in self.attributes[attr_b]:
                P_xy = self.joint_prob(attr_a, attr_a_value, attr_b, attr_b_value)
                total = total + (p_xy * log2(p_y / p_xy))

        return total


class DecisionTree():
    def __init__(examples):
        """
        Training
        * Start with a single root node
            * for each node (variable), if not pure (all poisonous or non poisonous), split by
            "best attribute", that is that split that:
                A: Maximizes information gain
                B: minimizes entropy after the split
            Stop when:
                A: the node is pure
                B: no attribute leads to positive informaiton gain

                information gain:
                    IG(X, Y) = H(X) - H(X|Y)
                    H(X) = sum[p(x)*log(px)]
                    H(Y|X) sum[p(x,y)*log(p(y)/p(x,y))]
        """
        self.root = Node(examples)


    def classify(example):
        """
        produce a classification based on a the n attributes of example
        """

        pass

classifier = DicisionTree()

def train(file):
    print "Training: %s" % file
    for item in reader.items():
        classifier.train(item)

    print "DONE"


def test(file):
    print "Training: %s" % file

    result = {True: {True: 0, False: 0},
             False: {True: 0, False: 0}}

    for item in reader.items():
        hypothesis = classifier.classify(item)

        result[hypothesis][hypothesis == item.poisonouse] = result[hypothesis][hypothesis == item.poisonouse] + 1

    accuracy = (result[True][True] + result[False][True]) / len(reader)
    print "Results: " 
    print "Accuracy:  %d  "  % accuracy


def validate(file):
    for item in reader.items():
        hypothesis = classifier.classify(item)


def run():
    pass

reader = Reader("noisy10_test.ssv")


