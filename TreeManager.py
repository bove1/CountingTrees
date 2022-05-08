from RootedTree import *
import numpy as np

class TreeManager:

    def __init__(self):
        self.trees_by_nodes = [[], [RootedTree(None, None, 1)]]
        self.canon_trees = [[], self.trees_by_nodes[1].copy()]
        self.layers = 1
        self.choose_dict = {}
        for i in range(17):
            print(f"Generating layer {self.layers}")
            self.generate_layer()
            print(len(self.trees_by_nodes[i]))
    
    def generate_layer(self):
        self.layers += 1
        trees_found = []
        for seq_count in [reshuffle(list, self.layers - 1) for list in generate_sequences(self.layers - 1)]:
            trees_each = [self.choose_with_dict(i + 1, j) for i, j in 
                        list(filter(lambda x: x[1] != 0, enumerate(seq_count)))]
            new_trees = [RootedTree(subtrees, self.trees_by_nodes, self.layers) #CHANGE BACK TO LAYERS - 1
                        for subtrees in prod(trees_each)]
            trees_found += new_trees
        self.trees_by_nodes.append(trees_found)
        self.canon_trees.append([tree for tree in trees_found if tree.canon])
        return trees_found

    def choose_with_dict(self, i, j):
        if (i, j) in self.choose_dict:
            return self.choose_dict[(i, j)]
        else:
            newval = choose(self.trees_by_nodes[i], j)
            self.choose_dict[(i, j)] = newval
            return newval

def generate_sequences(size, used=None, precalc={}):
    if used==None:
        used = size
    if size == 0:
        return [[]]
    possibles = []
    for i in range(1, used + 1):
        si = size - i
        mi = min(i, si)
        if (si, mi) in precalc:
            possibles += [[i] + seq for seq in precalc[si, mi]]
        else:
            newgen = generate_sequences(si, mi, precalc)
            precalc[(si, mi)] = newgen
            possibles += [[i] + seq for seq in newgen]
    return possibles

def reshuffle(list, max):
    new = [0 for _ in range(max)]
    for i in list:
        new[i - 1] += 1
    return new

def choose(list, count):
    if count ==1:
        return [[item] for item in list]
    chosen = []
    for i, item in enumerate(list):
        chosen += [[item] + seq for seq in choose(list[i:], count - 1)]
    return chosen

def prod(lists): #Think like a set product 
    if len(lists) == 1:
        return lists[0]
    else:
        return [item1 + later_list for item1 in lists[0] for later_list in prod(lists[1:])]

def main():
    trees = TreeManager()

    arr = np.array([
        [i for i, trees in enumerate(trees.canon_trees)],
        [len(trees) for i, trees in enumerate(trees.canon_trees)]
    ]).T
    np.savetxt('tree_counts.csv', arr, fmt="%d", delimiter=",")

    counts = np.array([len(trees) for i, trees in enumerate(trees.canon_trees)]).T
    counts[0] = 1

    tree_diameters = np.zeros((len(trees.canon_trees), len(trees.canon_trees)))
    for i, tree_list in enumerate(trees.canon_trees):
        for tree in tree_list:
            tree_diameters[tree.diameter_size][i] += 1
    tree_diameters /= counts
    np.savetxt('tree_diameters.csv', np.array(tree_diameters), delimiter=",")

    tree_degree = [[0 for _ in trees.canon_trees] for _ in trees.canon_trees]
    for i, tree_list in enumerate(trees.canon_trees):
        for tree in tree_list:
            tree_degree[tree.degree][i] += 1
    tree_degree /= counts
    np.savetxt('tree_degrees.csv', np.array(tree_degree), delimiter=",")

    tree_leaves = [[0 for _ in trees.canon_trees] for _ in trees.canon_trees]
    for i, tree_list in enumerate(trees.canon_trees):
        for tree in tree_list:
            tree_leaves[tree.leaves][i] += 1
    tree_leaves /= counts
    np.savetxt('tree_leaves.csv', np.array(tree_leaves), delimiter=",")

    


if __name__ == "__main__":
    main()