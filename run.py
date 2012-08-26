#!/usr/bin/en python

from dt import DecisionTree

class Reader():
    def __init__(self, file):
        pass

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


