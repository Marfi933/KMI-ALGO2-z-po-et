# Prvek B-stromu #
# Vycházel jsem z oficiálních algoritmů, ale struktury se liší z technických důvodu -> je to lehčí #
# Zkontroloval jsem si to na této stránce -> https://www.cs.usfca.edu/~galles/visualization/BTree.html #

class BNode:
    def __init__(self, leaf=False):
        self.leaf = leaf    # větev
        self.keys = []  # klíče
        self.child = []     # potomci

# B-strom

class BTree:
    def __init__(self, t):
        self.root = BNode(leaf=True)
        self.t = t

    def printTree(self, x, level=0):
        print("Vrstva/Level ", level, " ", len(x.keys), end=':')   # vypíše nám vrstvu, řadu prvků
        for i in x.keys:
            print(i, end='')
        print()
        level += 1
        if len(x.child) > 0:
            for i in x.child:
                self.printTree(i, level)


    def search(self, key, x=None):
        if x is not None:
            i = 0
            while i < len(x.keys) and key > x.keys[i][1]:   # x.keys[i][0] -> hledáme klíč na druhém místě -> první je index, len(x.keys) == n ze přednášky
                i += 1
            if i < len(x.keys) and key == x.keys[i][1]:
                return (x, i)
            elif x.leaf:
                return None
            else:
                return self.search(key, x.child[i])

        else:
            return self.search(key, self.root)

    def insert(self, key):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:  # klíče jsou zaplněné #
            s = BNode()
            self.root = s
            s.child.insert(0, root)
            self.split(s, 0)
            self.insert_non_full(s, key)
        else:
            self.insert_non_full(root, key)

    def insert_non_full(self, x, key):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append((None, None))     # první je index, druhý je klíč #
            while i >= 0 and key[0] < x.keys[i][0]:
                x.keys[i+1] = x.keys[i]
                i -= 1
            x.keys[i+1] = key
        else:
            while i >= 0 and key[0] < x.keys[i][0]:
                i -= 1
            i += 1
            if len(x.child[i].keys) == (2 * self.t) - 1:
                self.split(x, i)
                if key[0] > x.keys[i][0]:
                    i += 1
            self.insert_non_full(x.child[i], key)

    def split(self, x, i):
        t = self.t
        y = x.child[i]
        z = BNode(y.leaf)
        x.child.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]   # list -> (pro t = 2) prvni element rozdělí/vráti v listu #
        if not y.leaf:
            z.child = y.child[t: 2 * t]     # list -> (pro t = 2) třetí element rozdělí/vráti v listu -> záleží na t#
            y.child = y.child[0: t - 1]     # list -> (pro t = 2) prvni a druhý element rozdělí/vráti v listu #

    def create_empty_tree(self):
        x = BNode(leaf=True)
        self.root = x


B = BTree(2)

for i in range(10):
    B.insert((i, 2 * i))
B.printTree(B.root)

if B.search(20):
    print("Node is in B-tree")
else:
    print("Node isn't in B-tree")

if B.search(3):
    print("Node is in B-tree")
else:
    print("Node isn't in B-tree")



