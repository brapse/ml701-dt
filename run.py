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


