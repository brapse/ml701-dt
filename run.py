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

    pickle.dump(tree, open(options.filename, 'wb'))

    print "DONE"


EPSILON = 0.005
accuracy = 0

def prune():
    """
    for each node in the tree (bottom up vs top down)
        - evalute the accuracy of the tree with and without the node
            - if accuracy > EPSILON without => PRUNE
    """

    # top down
    # vs bottom up

    examples = pandas.read_csv(options.input, sep=' ',header=1, skiprows=[0,2])

    tree = pickle.load(open(options.filename, 'rb'))
    global accuracy
    accuracy = get_accuracy(tree, examples)

    def prune_top_down_recurse(node):
        print "Evaluating: %s" % str(node)
        global accuracy
        print "BEST %s" % accuracy
        for child in node.children:
            if child.leaf:
                continue

            child.leaf = True # fake prune
            accuracy_prime = get_accuracy(tree, examples)
            d_accuracy =  accuracy_prime - accuracy
            print "difference: %s " % d_accuracy
            if d_accuracy < EPSILON:
                child.leaf = False # unprune
                prune_top_down_recurse(child)
            else:
                accuracy = accuracy_prime

    def prune_bottom_up(node):
        print "Evaluating: %s" % str(node)
        global accuracy
        print "BEST %s" % accuracy
        for child in node.children:
            if child.leaf:
                continue

            prune_bottom_up(child)

            child.leaf = True # fake prune
            accuracy_prime = get_accuracy(tree, examples)
            d_accuracy =  accuracy_prime - accuracy

            print "difference: %s " % d_accuracy
            if d_accuracy < EPSILON:
                child.leaf = False # unprune
            else:
                accuracy = accuracy_prime

    print "Initial accuracy: %f" % accuracy

    prune_bottom_up(tree)

    print "Post pruning accuracy: %f" % accuracy

    pickle.dump(tree, open("pruned-bu.pkl", 'wb'))


def test_examples(tree, examples):
    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for x, item in examples.T.iteritems():
        hypothesis = tree.classify(item, 'poisonous')

        #print "poisonous: %s %s" % (item['poisonous'], hypothesis)

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

    return  {'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn}

def get_accuracy(tree, examples):
    result = test_examples(tree, examples)

    print result
    return (1.0 * result['tp'] + result['tn']) / sum(result.values())

def test():
    print "Testing: %s on %s" % (options.input, options.filename)

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

        #print "poisonous: %s %s" % (item['poisonous'], hypothesis)

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

    print "Tree: %s" % str(tree)

    print "Results: " 
    print "tp: %f" % tp
    print "tn: %f" % tn
    print "fp: %f" % fp
    print "fn: %f" % fn
    print "Accuracy:  %f  " % accuracy



try:
    if mode == "train":
        train()
    elif mode == "test":
        test()
    elif mode == "prune":
        prune()
    elif mode == "info":
        info()

except KeyboardInterrupt:
    print "EXIT"

"""
TODO:
    For full tree, top down pruned, bottom up pruned
        * size (number of nodes, depth)
        * training set accuracy
        * testing set accuracy

    For epsilon = 0:001; 0:005; 0:01; 0:03, top down and bottom up pruned
        * number of nodes pruned
"""
