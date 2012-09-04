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

    @property
    def leaves(self):
        return self.root.leaves

    @property
    def children(self):
        return self.root.children

    def prune(self):
        """
        Take a tree a remove branches that don't hurt the accuracy too much
        """
        pass

    def classify(self, example, var):
        """
        produce a classification based on a the n attributes of example
        """

        return self.root.classify(example, var)

    @property
    def size(self):
        def get_size(node):
            if node.leaf:
                return 1
            else:
                return 1 + sum([get_size(child) for child in node.children])

        return get_size(self.root)


    def __str__(self):
        return "<DecisionTree (%d nodes. %d deep)>" % (self.size, self.depth)


    @property
    def depth(self):
        def get_depth(node, current=0):
            if node.leaf:
                return current
            else:
                return max([get_depth(child, current+1) for child in node.children])

        return get_depth(self.root, 0)
