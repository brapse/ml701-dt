#!/usr/bin/en python


from optparse import OptionParser
from dt import DecisionTree
import pandas
import pickle

usage = "usage: %prog [options] train|test|ham|spam"

parser = OptionParser(usage=usage)

parser.add_option("-i", "--input", dest="input", default="data/noisy10_test.ssv",
                   help="input file Default: noisy10_test.ssv")

parser.add_option("-f", "--file", dest="filename", default="tree.pkl",
                   help="persist model to filename. Default: tree.pkl")

parser.add_option("-v", "--view", dest="view", default="normal",
                   help="Decorate the output. color, color-tokens or normal. Default: normal")

(options, args) = parser.parse_args()

if len(args) != 1:
    print "requires a mode, either \"train\" or \"test\""
    exit(1)
else:
    mode = args[0]


def train():
    print "Training: %s" % options.filename

    training = pandas.read_csv(options.input, sep=' ',header=1, skiprows=[0,2])
    tree = DecisionTree(training, 'poisonouse')
    tree.grow(0.01)

    filename = "tree.pkl"
    pickle.dump(tree, open(filename, 'wb'))

    print "DONE"


def test():
    print "Training: %s" % options.input

    testing  = pandas.read_csv(options.input, sep=' ',header=1, skiprows=[0,2])

    result = {True: {True: 0, False: 0},
             False: {True: 0, False: 0}}

    tp = 0
    tn = 0
    fp = 0
    fn = 0

    tree = pickle.load(open(options.filename, 'rb'))

    for x, item in testing.T.iteritems():
        hypothesis = tree.classify(item, 'poisonous')

        print "poisonous: %s %s" % (item['poisonous'], hypothesis)

        if hypothesis == item['poisonous']:
            if hypothesis:
                tp = tp + 1
            else:
                tn = tn + 1
        else:
            if hypothesis:
                fp = fp + 1
            else:
                fn = fp + 1

            
    accuracy = (1.0 * tp + tn) / len(testing)

    print "Results: " 
    print "tp: %f" % tp
    print "tn: %f" % tn
    print "fp: %f" % fp
    print "fn: %f" % fn
    print "Accuracy:  %f  "  % accuracy



try:
    if mode == "train":
        train()
    elif mode == "test":
        test()
except KeyboardInterrupt:
    print "EXIT"
