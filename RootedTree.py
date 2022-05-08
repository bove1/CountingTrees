
from doctest import master


class RootedTree:

    def __init__(self, subtrees: list, master_list, size):
        self.subtrees = subtrees
        self.master_list = master_list
        self.size = size
        self.canon = False
        self.calculate_diameters()
        self.calculate_max_degree()
        self.calculate_num_leaves()

    def calculate_diameters(self):
        if self.subtrees == None:
            self.diameter_size = 1
            self.length = 1
            self.canon = True

        else:
            self.subtrees = sorted(self.subtrees, key=lambda x: x.length)
            self.length = max([subtree.length for subtree in self.subtrees]) + 1
            pos_diameter = self.subtrees[-1].length + 1
            if len(self.subtrees) > 1:
                pos_diameter += self.subtrees[-2].length
            max_of_sub = max([subtree.diameter_size for subtree in self.subtrees])
            self.diameter_size = max([pos_diameter, max_of_sub])
            
            if pos_diameter >= max_of_sub: #Checks if on the diameter
                tallst = self.subtrees[-1].length
                if len(self.subtrees) >= 2:
                    second = self.subtrees[-2].length
                else:
                    second = 0
                if tallst == second:
                    self.canon = True
                elif tallst == second + 1:
                    self.canon = self.compare(self.subtrees[-1])
            if self.size == 2:
                self.canon = True
    pass

    def calculate_max_degree(self):
        if self.subtrees == None:
            self.degree = 0
        else:
            highest_prior = max([tree.degree for tree in self.subtrees])
            highest_of_sub = max([1] + [len(tree.subtrees) + 1 for tree in 
                self.subtrees if tree.subtrees != None])
            self.degree = max([len(self.subtrees), highest_prior, highest_of_sub])
    
    def calculate_num_leaves(self):
        if self.subtrees == None:
            self.non_self_leaves = 1
            self.leaves = 1
        else:
            self.non_self_leaves = sum([
                tree.non_self_leaves for tree in self.subtrees
                ])
            self.leaves = self.non_self_leaves
            if len(self.subtrees) == 1:
                self.leaves += 1

    def compare(self, other):
        non_largest_branch = self.subtrees[:-1]
        if other.subtrees is None:
            return False
        if len(non_largest_branch) < len(other.subtrees):
            return True
        elif len(other.subtrees) < len(non_largest_branch):
            return False
        for i, tree in enumerate(non_largest_branch):
            if other.subtrees[i] is not tree:
                other_size = other.subtrees[i].size
                if tree.size > other_size:
                    return True
                if other_size > tree.size:
                    return False
                
                tree_index = self.master_list[other_size].index(tree)
                other_index = self.master_list[other_size].index(other.subtrees[i])
                if tree_index > other_index:
                    return True
                else:
                    return False
        return True

    def set_size(self, size):
        self.size = size
        pass

    def __repr__(self):
        return self.string()

    def string(self, offset = 0):
        if self.size == 1:
            return '\n' + ''.join(['    ' for _ in range(offset)]) + 'NoneTree'
        return "\n" + ''.join(['    ' for _ in range(offset)]) \
             + 'Tree with:' \
                 + "".join([tree.string(offset=offset + 1) for tree in self.subtrees])
