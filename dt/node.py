import pandas
import math

def log2(num):
    return math.log(num) / math.log(2)


class Node(object):
    def __init__(self, examples,variable=None, value=None):
        """
        Build a dataframe
        """

        # pandas dataframe
        self.examples = examples

        self.children = []

        # Child properties
        self.variable = variable
        self.value = value

        self.max_ig = None
        self.predict_var = 'poisonous'


    def values(self, var):
        if var in self.variables():
            return set(self.examples[var].values)
        else:
            return set([])

    def variables(self):
        return set(self.examples.columns)

    def prob(self, var, value):
        return 1.0 * len(self.examples[self.examples[var] == value]) / len(self.examples)

    def joint_prob(self, v_a, i_a, v_b, i_b):
        return 1.0 * len(self.examples[(self.examples[v_a] == i_a) & (self.examples[v_b] == i_b)]) / len(self.examples)


    def information_gain(self, var_a, var_b):
        """ 
        Calculate the IG of the leaves accross attr
        IG(var_a, var_b) = H(var_a) - H(var_a|var_b)
        """
        a = self.entropy(var_a) 
        b = self.conditional_entropy(var_a, var_b)

        #print "E(%s): %f, E(%s|%s): %f" % (var_a, a, var_a, var_b, b)

        return a - b


    def entropy(self, var):
        """
        H(X) = sum[p(x)*log(px)]
        """
        total = 0

        for instance in self.values(var):
            total = total + self.prob(var, instance)*log2(self.prob(var, instance))

        return (-1) * total

    def conditional_entropy(self, attr_a, attr_b):
        """
        H(Y|X) = sum[p(x,y)*log(p(y)/p(x,y))]
        """

        total = 0
        for attr_a_value in self.values(attr_a):
            #p_y = self.prob(attr_a, attr_a_value)
            for attr_b_value in self.values(attr_b):
                p_x = self.prob(attr_b, attr_b_value)
                p_xy = self.joint_prob(attr_a, attr_a_value, attr_b, attr_b_value)
                #print "p(%s, %s) => %f" % (attr_a, attr_b, p_xy)
                if p_xy != 0:
                    total = total + (p_xy * log2(p_x / p_xy))

        return total

    @property
    def most_ig_var(self):
        if not self.max_ig:
            self.max_ig = self.calculate_max_ig()

        return self.max_ig[0]

    @property
    def most_ig_value(self):
        if not self.max_ig:
            self.max_ig = self.calculate_max_ig()

        return self.max_ig[1]


    def calculate_max_ig(self):
        max_ig = False
        for var in self.examples.columns:
            if var != self.predict_var:
                ig = self.information_gain(self.predict_var, var)
                #print "ig(poisonous, %s) => %f" % (var, ig)
                if not max_ig or ig > max_ig[1]:
                    max_ig = [var, ig]

        return max_ig

    
    def split(self, var):
        print "splitting: %s" % len(self.examples)
        def only_attr(value):
            return Node(self.examples[self.examples[var] == value], var, value)

        self.children = map(only_attr, self.values(var))


        return self.children

    def pure(self, var):
        return len(self.values(var)) == 1


    def classify(self, example, var):
        """
        Take an example, and a variable to predict,
        run it through the decision tree and predict the var of example
        """

        if len(self.children) == 0:
            if self.prob('poisonous', 1) > self.prob('poisonous', 0):
                return 1
            else:
                return 0
        else:
            for child in self.children:
                if child.value == example[child.variable]:
                    return child.classify(example, var)

if __name__ == "__main__":
    # Test
    data = pandas.read_csv('data/noisy10_test.ssv', sep=' ',header=1, skiprows=[0,2])
    n = Node(data)

    print "YO:%s" % n.values('poisonous')

    print "len(data): %s" % len(data)
    print "p(poisonous): %f " % n.prob('poisonous', 1)
    print "p(poisonous=1^capshape='f'): %f" % n.joint_prob('poisonous', 1, 'capshape', 'f')
    print "entropy(poisonous): %f" % n.entropy("poisonous")
    print "information_gain(poisonous, capshape): %f" % n.information_gain("poisonous", "capshape")
    print "most_ig: (%s => %f)" % (n.most_ig_var, n.most_ig_value)

    n.split(n.most_ig_var)

    for child in n.children:
        print "child (%s=%s) => (%s@%f)" % (child.variable, child.value, child.most_ig_var, child.most_ig_value)
