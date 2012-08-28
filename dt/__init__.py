from node import Node

class DecisionTree():
    def __init__(self, examples, predict_label):
        self.predict_label = predict_label
        self.root = Node(examples)


    def grow(self, threshold):
        """
        Growing
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

        def split(tree, var):
            print "Branching: %s" % var
            for branch in tree.split(var):
                if not branch.pure(self.predict_label) and branch.most_ig_value > threshold:
                    split(branch, branch.most_ig_var)

        split(self.root, self.root.most_ig_var)


    def prune(self):
        pass

    def classify(self, example, var):
        """
        produce a classification based on a the n attributes of example
        """

        return self.root.classify(example, var)
